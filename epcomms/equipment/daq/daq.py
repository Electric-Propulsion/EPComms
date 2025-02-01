# pylint: disable=missing-module-docstring
# TODO: add module docstring # pylint: disable=fixme

from abc import abstractmethod
from typing import Union
from epcomms.equipment.base import Instrument


class DAQ(Instrument):
    """Abstract class for all DAQ modules."""

    ####################
    # Oscilloscope
    ####################

    @abstractmethod
    def scope_open(self, sampling_frequency: float, buffer_size: int, offset: int, amplitude_range: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def scope_close(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def scope_measure(self, channel: int) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def scope_record(self, channel: int) -> list[float]:
        raise NotImplementedError
    
    @abstractmethod
    def scope_trigger(self, channel: int, source: str, enable: bool, level: float, edge_rising: bool = True) -> list[float]:
        raise NotImplementedError
    
    ####################
    # Signal Generator
    ####################

    @abstractmethod
    def wavegen_open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def wavegen_close(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def wavegen_generate(self, channel: int, function: str, offset: float, frequency: float, amplitude: float, symmetry: float, wait_time: float, run_time: float, repeat_count: float, input_data: list[float]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def wavegen_enable_channel(self, channel: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def wavegen_disable_channel(self, channel: int) -> None:
        raise NotImplementedError
    
    ####################
    # Power Supply
    ####################

    @abstractmethod
    def psu_open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def psu_close(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def psu_switch(self) -> None:
        # Todo define params if needed
        raise NotImplementedError
    
    ####################
    # Multimeter
    ####################

    @abstractmethod
    def dmm_open(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def dmm_close(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def dmm_measure(self, mode: str, range: float, high_impedance: bool) -> None:
        raise NotImplementedError