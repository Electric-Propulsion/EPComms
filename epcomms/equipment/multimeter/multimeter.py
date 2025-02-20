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
    def measure_voltage_ac(self, measurement_range, resolution) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_voltage_dc(self, measurement_range, resolution) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_capacitance(self, measurement_range, resolution) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_continuity(self) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def measure_current_ac(self, measurement_range, resolution) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def measure_current_dc(self, measurement_range, resolution) -> float:
        raise NotImplementedError
        
    @abstractmethod
    def measure_frequency(self, freq_range, freq_resolution, volt_range) -> float:
        raise NotImplementedError