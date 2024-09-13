from epcomms.equipment.base import Instrument
from abc import abstractmethod


class FlowController(Instrument):

    @abstractmethod
    def get_pressure(self) -> float:
        raise NotImplementedError("Calling abstract method!")

    @abstractmethod
    def get_setpoint(self) -> float:
        raise NotImplementedError("Calling abstract method!")

    @abstractmethod
    def set_setpoint(self, setpoint: float) -> None:
        raise NotImplementedError("Calling abstract method!")
