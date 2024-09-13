from . import Transmission
import pyvisa
from epcomms.connection.packet import Packet, ASCII


class Visa(Transmission):

    device: pyvisa.resources

    @classmethod
    def list_resources(cls) -> list:
        return pyvisa.ResourceManager().list_resources()

    def __init__(self, resource_name: str) -> None:
        self.device = pyvisa.ResourceManager().open_resource(resource_name)
        super().__init__(ASCII)

    def command(self, data: ASCII) -> None:
        assert isinstance(data, ASCII)
        self.device.write(data.serialize_str())

    def read(self) -> Packet:
        packet = self.packet_class(self.device.read())
        return packet
