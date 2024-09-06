from . import Transmission
import pyvisa
from epcomms.connection.packet import ASCII


class Visa(Transmission):

    device: pyvisa.resources
    Packet = ASCII

    @classmethod
    def list_resources(cls) -> list:
        return pyvisa.ResourceManager().list_resources()

    def __init__(self, resource_name: str) -> None:
        super().__init__()
        self.device = pyvisa.ResourceManager().open_resource(resource_name)

    def command(self, data: str) -> None:
        packet = self.Packet(data)
        self.device.write(packet.serialize_str())

    def read(self) -> str:
        packet = self.Packet(self.device.read())
        return packet.data
