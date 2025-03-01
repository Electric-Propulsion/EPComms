"""
This module defines the abstract base class `PowerSupply` for all power supplies.
"""

from abc import abstractmethod
from typing import Union
from epcomms.equipment.base import Instrument


class PowerSupply(Instrument):
    """Abstract Base Class for all Power Supplies."""

    @abstractmethod
    def set_voltage(self, voltage: float, channel: Union[int, list[int]]) -> None:
        """Set the voltage of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def measure_voltage_setpoint(self, channel: Union[int, list[int]]) -> float:
        """Measure the voltage of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def measure_voltage(self, channel: Union[int, list[int]]) -> float:
        """Measure the voltage of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def set_current_limit(self, current: float, channel: Union[int, list[int]]) -> None:
        """Set the current of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def measure_current_limit(self, channel: Union[int, list[int]]) -> float:
        """Measure the current of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def measure_current(self, channel: Union[int, list[int]]) -> float:
        """Measure the current of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def get_output(self, channel: Union[int, list[int]]) -> None:
        """Get the output status of the power supply."""
        raise NotImplementedError

    @abstractmethod
    def set_output(self, state: bool, channel: Union[int, list[int]]) -> None:
        """Set the output of the power supply."""
        raise NotImplementedError
