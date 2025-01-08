from serial import Serial as Pyserial
from epcomms.connection.packet import ASCII
from . import Transmission, TransmissionError

class Serial(Transmission):
    
    def __init__(self, device: str, baud: int = 9600, terminator = '\r\n'):
        self.driver = Pyserial(device, baud)
        self.terminator = terminator.encode("ascii")
        super().__init__(ASCII)

    def _command(self, data: ASCII) -> None:
        assert isinstance(data, self.packet_class)
        self.driver.write(data.serialize_bytes())

    def _read(self) -> ASCII:
        data = self.driver.readline()#(self.terminator)
        packet = self.packet_class(data.decode("ascii")[0:-len(self.terminator)])
        return packet