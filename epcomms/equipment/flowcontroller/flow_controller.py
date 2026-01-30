from abc import abstractmethod

from epcomms.equipment.base import Instrument, TransmissionTypeT


class FlowController(Instrument[TransmissionTypeT]):
    """
    Abstract base class for all flow controllers.
    """

    @abstractmethod
    def get_pressure(self) -> float:
        """
        Get the pressure from the flow controller.

        Returns:
            float: The current pressure from the flow controller.
        """
        raise NotImplementedError("Calling abstract method!")

    @abstractmethod
    def get_setpoint(self) -> float:
        """
        Retrieve the setpoint value of the flow controller.

        Returns:
            float: The setpoint value of the flow controller.
        """
        raise NotImplementedError("Calling abstract method!")

    @abstractmethod
    def set_setpoint(self, setpoint: float) -> None:
        """
        Set the setpoint for the flow controller.

        Args:
            setpoint (float): The desired setpoint value for the flow controller.
        """
        raise NotImplementedError("Calling abstract method!")
