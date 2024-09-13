"""
Module: flow_controller
This module defines the FlowController class, which is an abstract base class for flow controllers. 
It inherits from the Instrument class and provides abstract methods that must be implemented by 
subclasses to interact with flow controllers.
"""

from abc import abstractmethod
from epcomms.equipment.base import Instrument


class FlowController(Instrument):
    """
    FlowController is an abstract base class that represents a flow controller instrument.
    It inherits from the Instrument class and defines the following abstract methods:
    Methods
    -------
    get_pressure() -> float
        Abstract method to get the current pressure. Must be implemented by subclasses.
    get_setpoint() -> float
        Abstract method to get the current setpoint. Must be implemented by subclasses.
    set_setpoint(setpoint: float) -> None
        Abstract method to set a new setpoint. Must be implemented by subclasses.
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
