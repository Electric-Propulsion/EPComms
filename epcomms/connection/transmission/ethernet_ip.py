from pycomm3 import CIPDriver, Services
from pycomm3.tag import Tag

from epcomms.connection.packet import CIPRX, CIPTX

from .transmission import Transmission, TransmissionError


class EthernetIP(Transmission[CIPRX, CIPTX]):
    """class for communication with EtherNet/IP devices
    Fun fact: The 'IP' in EtherNet/IP stands for 'Industrial Protocol' and not 'Internet Protocol'
    """

    # The driver object for the pycomm3 library
    driver: CIPDriver

    def __init__(self, device_path: str):
        """Initializes the EthernetIP object
        Args:
            device_path (str): The path to the device, e.g. '192.168.0.172'
        """
        self.driver = CIPDriver(device_path)
        super().__init__()

    def _command(self, packet: CIPTX):
        """Send a command to the device

        Args:
            data (CIPTX): The data to send to the device
        """
        if not self.driver.connected:
            self.driver.open()
        serialized_packet = packet.serialize()
        response_tag: Tag = (
            self.driver.generic_message(  # pyright: ignore[reportUnknownMemberType]
                service=Services.set_attribute_single,
                class_code=serialized_packet["class_code"],
                instance=serialized_packet["instance"],
                attribute=serialized_packet["attribute"],
                request_data=serialized_packet["request_data"],
            )
        )

        if not response_tag:
            raise TransmissionError(
                f"EtherNet/IP command failed for "
                f"class_code={serialized_packet['class_code']}, "
                f"instance={serialized_packet['instance']}, "
                f"attribute={serialized_packet['attribute']}"
            )

    def _read(self) -> CIPRX:
        raise NotImplementedError(
            "EthernetIP does not support read operations. You must poll for data."
        )

    def poll(self, packet: CIPTX) -> CIPRX:
        """Poll the device for data

        Args:
            data (CIPTX): The data to poll for

        Returns:
            CIPRX: The data received from the device
        """
        if not self.driver.connected:
            self.driver.open()

        serialized_packet = packet.serialize()
        response_tag = (
            self.driver.generic_message(  # pyright: ignore[reportUnknownMemberType]
                service=Services.get_attribute_single,
                class_code=serialized_packet["class_code"],
                instance=serialized_packet["instance"],
                attribute=serialized_packet["attribute"],
                data_type=serialized_packet["data_type"],
            )
        )

        if not response_tag:
            raise TransmissionError(
                f"EtherNet/IP poll failed: empty response for "
                f"class_code={serialized_packet['class_code']}, "
                f"instance={serialized_packet['instance']}, "
                f"attribute={serialized_packet['attribute']}"
            )

        return CIPRX.from_wire(response_tag)
