"""
This module provides the Visa class for handling VISA 
(Virtual Instrument Software Architecture) communication.
"""

import pyvisa
from epcomms.connection.packet import Packet, ASCII
from . import Transmission
from threading import Lock
import time


class Visa(Transmission):
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

    class_lock: Lock = Lock()

    @classmethod
    def list_resources(cls) -> list:
        """
        List available VISA resources.

        This class method uses the PyVISA library to retrieve a list of available
        VISA (Virtual Instrument Software Architecture) resources connected to the system.

        Returns:
            list: A list of strings, each representing a VISA resource identifier.
        """
        # return pyvisa.ResourceManager().list_resources()
        cls.class_lock.acquire()
        resources = pyvisa.ResourceManager("@py").list_resources()
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
        self.device: pyvisa.resources = None

        for i in range(10):
            try:
                # self.device = pyvisa.ResourceManager().open_resource(resource_name)
                self.class_lock.acquire()
                self.device = pyvisa.ResourceManager("@py").open_resource(resource_name)
            except pyvisa.errors.VisaIOError as e:
                if i >= 9:
                    raise(e)
                continue
            finally:
                self.class_lock.release()
            break
        self.device.timeout = 2500
        super().__init__(ASCII)

    def _command(self, data: ASCII) -> None:
        """
        Sends a command to the device.

        Parameters:
        data (ASCII): The ASCII data to be sent to the device.
            Must be an instance of the ASCII class.

        Raises:
        AssertionError: If the provided data is not an instance of the ASCII class.
        """
        assert isinstance(data, ASCII)
        try:
            self.device.write(data.serialize_str())
        except Exception as e:
            raise e

    def _read(self) -> Packet:
        """
        Reads data from the device and returns it as a Packet object.

        Returns:
            Packet: The data read from the device, encapsulated in a Packet object.
        """
        try:
            packet = self.packet_class(self.device.read())
        except Exception as e:
            raise e
        
        return packet
    
    def poll(self, data: ASCII) -> Packet:
        with self._lock:
            try:
                return self.packet_class(self.device.query(data.serialize_str()))
            except Exception as e:
                raise e
    
    def close(self) -> None:
        self.device.close()
