from serial import Serial as Pyserial

from epcomms.connection.packet import ASCII

from .transmission import Transmission


class Serial(Transmission[ASCII, ASCII]):

    def __init__(self, device: str, baud: int = 9600, terminator: str = "\r\n"):
        self.driver = Pyserial(device, baud)
        self.terminator = terminator.encode("ascii")
        super().__init__()

    def _command(self, packet: ASCII) -> None:
        self.driver.write(packet.serialize())

    def _read(self) -> ASCII:
        data = self.driver.readline()  # (self.terminator)
        packet = ASCII.from_wire(data[0 : -len(self.terminator)])
        return packet
