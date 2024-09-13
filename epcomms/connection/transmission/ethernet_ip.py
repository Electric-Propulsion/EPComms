"""
This module provides the EthernetIP class for communication with EtherNet/IP devices.
Classes:
    EthernetIP: A class for communication with EtherNet/IP devices.
Exceptions:
    TransmissionError: Raised when there is an error in transmission.
Dependencies:
    - Transmission, TransmissionError from the same package.
    - CIPRX, CIPTX from epcomms.connection.packet.
    - CIPDriver, Services from pycomm3.
Classes:
    EthernetIP(Transmission):
        A class for communication with EtherNet/IP devices.
        Attributes:
            driver (CIPDriver): The driver object for the pycomm3 library.
        Methods:
            __init__(self, device_path):
                Initializes the EthernetIP object.
                    device_path (str): The path to the device, e.g. '192.168.0.172'.
            command(self, data: CIPTX):
                Sends a command to the device.
                    data (CIPTX): The data to send to the device.
            read(self):
                Raises NotImplementedError as EthernetIP does not support read operations.
            poll(self, data: CIPTX) -> CIPRX:
                Polls the device for data.
                    data (CIPTX): The data to poll for.
                    CIPRX: The data received from the device.
"""

from pycomm3 import CIPDriver, Services
from epcomms.connection.packet import CIPRX, CIPTX
from . import Transmission, TransmissionError


class EthernetIP(Transmission):
    """class for communication with EtherNet/IP devices
    Fun fact: The 'IP' in EtherNet/IP stands for 'Industrial Protocol' and not 'Internet Protocol'
    """

    # The driver object for the pycomm3 library
    driver: CIPDriver

    def __init__(self, device_path):
        """Initializes the EthernetIP object
        Args:
            device_path (str): The path to the device, e.g. '192.168.0.172'
        """
        self.driver = CIPDriver(device_path)
        super().__init__(CIPRX)

    def command(self, data: CIPTX):
        """Send a command to the device

        Args:
            data (CIPTX): The data to send to the device
        """
        if not self.driver.connected:
            self.driver.open()

        print(data.data)

        repsonse_tag = self.driver.generic_message(
            service=Services.set_attribute_single,
            class_code=data.class_code,
            instance=data.instance,
            attribute=data.attribute,
            request_data=data.parameters,
        )

        if not repsonse_tag:
            print(repsonse_tag)
            raise TransmissionError()

    def read(self):
        raise NotImplementedError(
            "EthernetIP does not support read operations. You must poll for data."
        )

    def poll(self, data: CIPTX) -> CIPRX:
        """Poll the device for data

        Args:
            data (CIPTX): The data to poll for

        Returns:
            CIPRX: The data received from the device
        """
        if not self.driver.connected:
            self.driver.open()

        response_tag = self.driver.generic_message(
            service=Services.get_attribute_single,
            class_code=data.class_code,
            instance=data.instance,
            attribute=data.attribute,
            data_type=data.data_type,
        )

        if not response_tag:
            raise TransmissionError()

        return self.packet_class(response_tag)
