"""
This module provides the Visa class for handling VISA
(Virtual Instrument Software Architecture) communication.
"""

import time
from threading import Lock
from typing import ClassVar

from gpib_ctypes import make_default_gpib
make_default_gpib()

import pyvisa



from epcomms.connection.packet import String

from .transmission import Transmission


class Visa(Transmission[String, String]):
    """
    Visa class for handling communication with VISA-compatible devices using the pyvisa library.
    Attributes:
        device (pyvisa.resources): The VISA resource representing the connected device.
    Methods:
        list_resources() -> list:
            Class method that lists all available VISA resources.
        __init__(resource_name: str) -> None:
            Initializes the Visa object and opens a connection to the specified VISA resource.
        command(data: ASCII) -> None:
            Sends a command to the connected device.
        read() -> Packet:
            Reads data from the connected device and returns it as a Packet object.
    """

    class_lock: ClassVar[Lock] = Lock()
    resource_manager = pyvisa.ResourceManager("@py")
    device: pyvisa.resources.MessageBasedResource

    @classmethod
    def list_resources(cls) -> tuple[str, ...]:
        """
        List available VISA resources.

        This class method uses the PyVISA library to retrieve a list of available
        VISA (Virtual Instrument Software Architecture) resources connected to the system.

        Returns:
            list: A list of strings, each representing a VISA resource identifier.
        """
        # return pyvisa.ResourceManager().list_resources()
        cls.class_lock.acquire()
        resources = cls.resource_manager.list_resources("?*")
        cls.class_lock.release()
        return resources

    def __init__(self, resource_name: str) -> None:
        """
        Initializes a connection to a VISA resource.

        Args:
            resource_name (str): The resource name of the VISA device to connect to.

        Returns:
            None
        """
        num_attempts = 10
        for i in range(num_attempts):
            try:
                time.sleep(0.1)
                with self.class_lock:
                    device = self.resource_manager.open_resource(
                        resource_name,
                    )
                    if not isinstance(device, pyvisa.resources.MessageBasedResource):
                        raise TypeError(
                            "The opened resource is not a MessageBasedResource."
                        )
                    self.device = device
            except pyvisa.errors.VisaIOError as e:
                if i == num_attempts - 1:
                    raise (e)
                else:
                    continue
            break
        self.device.timeout = 2500
        super().__init__()

    def _command(self, packet: String) -> None:
        """
        Sends a command to the device.

        Parameters:
        data (ASCII): The ASCII data to be sent to the device.
            Must be an instance of the ASCII class.

        Raises:
        AssertionError: If the provided data is not an instance of the ASCII class.
        """
        try:
            self.device.write(packet.serialize())
        except Exception as e:
            raise e

    def _read(self) -> String:
        """
        Reads data from the device and returns it as a Packet object.

        Returns:
            Packet: The data read from the device, encapsulated in a Packet object.
        """
        try:
            packet = String.from_wire(self.device.read())
        except Exception as e:
            raise e

        return packet

    def poll(self, packet: String) -> String:
        with self._lock:
            try:
                return String.from_wire(self.device.query(packet.serialize()))
            except Exception as e:
                raise e

    def close(self) -> None:
        self.device.close()
