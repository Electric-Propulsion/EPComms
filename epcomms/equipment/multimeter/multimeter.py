"""
This module defines the abstract base class `Multimeter` for all multimeters.
"""
# pylint: disable=missing-module-docstring

from abc import abstractmethod
from typing import Union
from epcomms.equipment.base import Instrument


class Multimeter(Instrument):
    """Abstract class for all multimeters."""

    @abstractmethod
    def measure_voltage_ac(self, range, resolution, channel) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_voltage_dc(self, range, resolution, channel) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_capacitance(self, range, resolution) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_continuity(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_current_ac(self, range, resolution, channel) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_current_dc(self, range, resolution, channel) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_diode(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_frequency(self, range, resolution, channel) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_resistance(self, range, resolution, channel) -> float:
        raise NotImplementedError
