from abc import ABC, abstractmethod


class Transmission(ABC):

    @abstractmethod
    def command(self, data: str) -> None:
        """Send a packet of data to the connected device, i.e. 'transmit' data."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def read(self) -> str:
        """Recieve a packet of data from the connected device."""
        raise NotImplementedError("This is an abstract method!")

    def poll(self, data: str) -> str:
        """Default implementation of 'polling' for data, should be overridden
        if a transmission method has a more efficient way to poll."""

        self.command(data)
        return self.read()
