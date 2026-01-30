from abc import ABC, abstractmethod
from threading import Lock
from typing import Any, Generic, TypeVar

from epcomms.connection.packet.packet import ReceivedPacket, TransmittedPacket

RXPacketT = TypeVar("RXPacketT", bound=ReceivedPacket[Any, Any])
# pylint: disable=invalid-name
# unfortunately there is no way for me to talk about transmitted packets
# without starting the variable name with a capital T
TXPacketT = TypeVar("TXPacketT", bound=TransmittedPacket[Any, Any])


class TransmissionError(Exception):
    """Custom exception for transmission-related errors."""


class Transmission(ABC, Generic[RXPacketT, TXPacketT]):
    """Abstract base class for handling packet transmission."""

    def __init__(self) -> None:
        self._lock: Lock = Lock()

    @abstractmethod
    def _command(self, packet: TXPacketT) -> None:
        """
        Send a packet of data to the connected device, i.e. 'transmit' data.

        This is the internal method that actual implementations should override.
        """
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def _read(self) -> RXPacketT:
        """
        Receive a packet of data from the connected device.

        This is the internal method that actual implementations should override.

        """
        raise NotImplementedError("This is an abstract method!")

    def command(self, packet: TXPacketT) -> None:
        """
        Send a packet of data to the connected device.

        This is the thread-safe public method that wraps the internal _command method.
        """
        with self._lock:
            self._command(packet)

    def read(self) -> RXPacketT:
        """
        Receive a packet of data from the connected device.

        This is the thread-safe public method that wraps the internal _read method.
        """
        with self._lock:
            return self._read()

    def poll(self, packet: TXPacketT) -> RXPacketT:
        """Default implementation of 'polling' for data, should be overridden
        if a transmission method has a more efficient way to poll."""

        with self._lock:
            self._command(packet)
            return self._read()

    def close(self) -> None:
        """
        Safely close the transmission.

        This method can be overridden by subclasses to implement specific closing behavior.
        """
