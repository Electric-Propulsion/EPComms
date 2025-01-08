"""
This module defines the Transmission abstract base class and the TransmissionError exception.
Classes:
    TransmissionError: Custom exception for transmission-related errors.
    Transmission: Abstract base class for handling packet transmission.
The Transmission class requires a packet_class argument during initialization, 
which must be a subclass of Packet.
It provides abstract methods for sending and receiving packets, and a default 
implementation for polling data.
Methods:
    __init__(self, packet_class: type) -> None:
        Initializes the Transmission object with the specified packet class.
    command(self, data: Packet) -> None:
        Abstract method to send a packet of data to the connected device.
    read(self) -> Packet:
        Abstract method to receive a packet of data from the connected device.
    poll(self, data: Packet) -> Packet:
        Sends a packet of data and waits for a response, using the default implementation.
"""

from abc import ABC, abstractmethod
from epcomms.connection.packet import Packet
import time
from threading import Lock


class TransmissionError(Exception):
    """Custom exception for transmission-related errors."""


class Transmission(ABC):
    """Abstract base class for handling packet transmission."""

    packet_class: type

    def __init__(self, packet_class: type) -> None:
        # TODO: Is there a way to type hint this? # pylint: disable=fixme
        # TODO: We should check if the packet is concrete # pylint: disable=fixme
        # TODO: Is there a way to check this without instantiating the object? # pylint: disable=fixme #(I'm working on it!)
        if not issubclass(packet_class, Packet):
            raise TypeError("packet_class must be of type Packet")

        self.packet_class = packet_class
        self._lock = Lock()

    @abstractmethod
    def _command(self, data: Packet) -> None:
        """Send a packet of data to the connected device, i.e. 'transmit' data."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def _read(self) -> Packet:
        """Recieve a packet of data from the connected device."""
        raise NotImplementedError("This is an abstract method!")

    def command(self, data: Packet) -> None:
        with self._lock:
            self._command(data)
    
    def read(self) -> Packet:
        with self._lock:
            return self._read()


    def poll(self, data: Packet) -> Packet:
        """Default implementation of 'polling' for data, should be overridden
        if a transmission method has a more efficient way to poll."""

        with self._lock:
            self._command(data)
            return self._read()

    def close(self) -> None:
        pass