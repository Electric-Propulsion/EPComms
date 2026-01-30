import time
from threading import Lock
from typing import ClassVar, Optional

import pyvisa

from epcomms.connection.packet import String

from .transmission import Transmission


class Visa(Transmission[String, String]):
    """
    Visa class for handling communication with VISA-compatible devices using the pyvisa library.
    """

    class_lock: ClassVar[Lock] = Lock()
    resource_manager = pyvisa.ResourceManager("@py")
    device: pyvisa.resources.MessageBasedResource
    terminator: Optional[str]

    @classmethod
    def list_resources(cls) -> tuple[str, ...]:
        """
        List available VISA resources.

        This class method uses the PyVISA library to retrieve a list of available
        VISA resources connected to the system.

        Returns:
            list: A list of strings, each representing a VISA resource identifier.
        """
        with cls.class_lock:
            resources = cls.resource_manager.list_resources("?*")
        return resources

    def __init__(self, resource_name: str, terminator: Optional[str] = None) -> None:
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
                    raise e
            break
        self.device.timeout = 2500
        self.terminator = terminator
        super().__init__()

    def _command(self, packet: String) -> None:
        try:
            self.device.write(packet.serialize(), termination=self.terminator)
        except Exception as e:
            raise e

    def _read(self) -> String:
        try:
            packet = String.from_wire(self.device.read(termination=self.terminator))
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
