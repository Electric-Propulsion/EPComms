import telnetlib

from . import Transmission, TransmissionError

from epcomms.connection.packet import Packet

class Telnet(Transmission):

    def __init__(self, host: str, port: int, terminator: str, packet_class: type):
        self.driver = telnetlib.Telnet(host, port)
        self.terminator = terminator.encode("ascii")
        super().__init__(packet_class)


    def _command(self, data: Packet) -> None:
        assert isinstance(data, self.packet_class)
        self.driver.write(data.serialize_bytes()+self.terminator)

    def _read(self) -> Packet:
        data = self.driver.read_until(self.terminator)
        packet = self.packet_class(data.decode("ascii")[0:-len(self.terminator)])
        return packet





