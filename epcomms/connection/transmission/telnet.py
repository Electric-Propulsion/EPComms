import socket

# pylint: disable=deprecated-module
# TODO: Replace telnetlib with a modern alternative # pylint: disable=fixme
import telnetlib

from epcomms.connection.packet import ASCII

from .transmission import Transmission


class Telnet(Transmission[ASCII, ASCII]):
    """Telnet transmission class using telnetlib"""

    def __init__(self, host: str, port: int, terminator: str, timeout: float):
        self.driver = telnetlib.Telnet(host, port, timeout)
        self._timeout = timeout
        self.terminator = terminator.encode("ascii")
        super().__init__()

    def _command(self, packet: ASCII) -> None:
        self.driver.write(packet.serialize() + self.terminator)

    def _read(self) -> ASCII:
        data = self.driver.read_until(self.terminator, self._timeout)
        packet = ASCII.from_wire(data[0 : -len(self.terminator)])
        return packet

    def close(self):
        self.driver.get_socket().shutdown(socket.SHUT_WR)
        self.driver.read_all()
        self.driver.close()
