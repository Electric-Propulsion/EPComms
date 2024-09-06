from abc import abstractmethod
from epcomms.equipment.base import Controller, Instrument


class PowerSupply(Controller, Instrument):
    def __init__(self, transmission) -> None:
        self.transmission = transmission
        super().__init__()

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
