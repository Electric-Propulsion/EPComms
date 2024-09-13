from abc import ABC, abstractmethod
from epcomms.connection.packet import Packet


class TransmissionError(Exception):
    pass


class Transmission(ABC):

    packet_class: type

    def __init__(self, packet_class: type) -> None:
        # TODO: Is there a way to type hint this?
        # TODO: We should check if the packet is concrete
        # TODO: Is there a way to check this without instantiating the object?
        if not issubclass(packet_class, Packet):
            raise TypeError("packet_class must be of type Packet")

        self.packet_class = packet_class

    @abstractmethod
    def command(self, data: Packet) -> None:
        """Send a packet of data to the connected device, i.e. 'transmit' data."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def read(self) -> Packet:
        """Recieve a packet of data from the connected device."""
        raise NotImplementedError("This is an abstract method!")

    def poll(self, data: Packet) -> Packet:
        """Default implementation of 'polling' for data, should be overridden
        if a transmission method has a more efficient way to poll."""

        self.command(data)
        return self.read()
