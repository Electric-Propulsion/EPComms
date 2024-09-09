from . import Transmission
import pyvisa
from epcomms.connection.packet import ASCII


class Visa(Transmission):

    device: pyvisa.resources

    @classmethod
    def list_resources(cls) -> list:
        return pyvisa.ResourceManager().list_resources()

    def __init__(self, resource_name: str) -> None:
        self.device = pyvisa.ResourceManager().open_resource(resource_name)
        super().__init__(ASCII)

    def command(self, data: str) -> None:
        packet = self.packet_class(data)
        self.device.write(packet.serialize_str())

    def read(self) -> str:
        packet = self.packet_class(self.device.read())
        return packet.data
