"""
This module defines the abstract base class `TemperatureSensor` for all temperature sensors.
"""

from abc import abstractmethod
from epcomms.equipment.base import Instrument


class TemperatureSensor(Instrument):
    """Abstract Base Class for all Power Supplies."""

    @abstractmethod
    def open_instrument(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def close_instrument(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def enable_sampling(self, sampling_interval: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def disable_sampling(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def configure_channel(self, channel: int, type: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def disable_channel(self, channel: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def measure_temperature(self, channel: int) -> float:
        raise NotImplementedError