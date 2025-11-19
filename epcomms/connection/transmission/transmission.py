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
from threading import Lock
from typing import Any, Generic, TypeVar

from epcomms.connection.packet.packet import ReceivedPacket, TransmittedPacket

RX_Packet = TypeVar("RX_Packet", bound=ReceivedPacket[Any, Any])
TX_Packet = TypeVar("TX_Packet", bound=TransmittedPacket[Any, Any])


class TransmissionError(Exception):
    """Custom exception for transmission-related errors."""


class Transmission(ABC, Generic[RX_Packet, TX_Packet]):
    """Abstract base class for handling packet transmission."""

    def __init__(self) -> None:
        self._lock: Lock = Lock()

    @abstractmethod
    def _command(self, packet: TX_Packet) -> None:
        """Send a packet of data to the connected device, i.e. 'transmit' data."""
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def _read(self) -> RX_Packet:
        """Recieve a packet of data from the connected device."""
        raise NotImplementedError("This is an abstract method!")

    def command(self, packet: TX_Packet) -> None:
        with self._lock:
            self._command(packet)

    def read(self) -> RX_Packet:
        with self._lock:
            return self._read()

    def poll(self, packet: TX_Packet) -> RX_Packet:
        """Default implementation of 'polling' for data, should be overridden
        if a transmission method has a more efficient way to poll."""

        with self._lock:
            self._command(packet)
            return self._read()

    def close(self) -> None:
        pass
