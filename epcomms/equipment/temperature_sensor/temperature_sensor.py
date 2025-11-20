"""
This module defines the abstract base class `TemperatureSensor` for all temperature sensors.
"""

from abc import abstractmethod

from epcomms.equipment.base import Instrument, TransmissionType


class TemperatureSensor(Instrument[TransmissionType]):
    """Abstract Base Class for all Power Supplies."""

    @abstractmethod
    def open_instrument(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close_instrument(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def configure_channel(self, channel: int, channel_type: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def disable_channel(self, channel: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def measure_temperature(self, channel: int) -> float:
        raise NotImplementedError
