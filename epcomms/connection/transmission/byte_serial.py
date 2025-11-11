from serial import Serial as Pyserial
from epcomms.connection.packet import Bytes
from .transmission import Transmission, TransmissionError

class ByteSerial(Transmission):
    
    def __init__(self, device: str, baud: int = 9600, terminator = '\r\n'):
        self.driver = Pyserial(device, baud)
        self.terminator = terminator.encode("ascii")
        super().__init__(Bytes)

    def _command(self, data: Bytes) -> None:
        assert isinstance(data, self.packet_class)
        self.driver.write(data.serialize_bytes())

    def _read(self) -> Bytes:
        # read until a 9-byte packet that starts with bytes 0x07,0x05 is found
        while True:
            first = self.driver.read(1)
            if first == b'\x07':
                second = self.driver.read(1)
                if second == b'\x05':
                    rest = self.driver.read(7)
                    data = first + second + rest
                    break
        packet = self.packet_class(data)
        return packet