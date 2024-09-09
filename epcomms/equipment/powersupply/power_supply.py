from abc import ABC, abstractmethod
from epcomms.equipment.base import Instrument


class PowerSupply(Instrument):
    def __init__(self, transmission) -> None:
        super().__init__(transmission)

    @abstractmethod
    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        raise NotImplementedError

    @abstractmethod
    def measure_voltage(self, channel: int = 0) -> float:
        raise NotImplementedError

    @abstractmethod
    def set_current(self, current: float, channel: int = 0) -> None:
        raise NotImplementedError

    @abstractmethod
    def measure_current(self, channel: int = 0) -> float:
        raise NotImplementedError

    @abstractmethod
    def enable_output(self, channel: int = 0) -> None:
        raise NotImplementedError

    @abstractmethod
    def disable_output(self, channel: int = 0) -> None:
        raise NotImplementedError
