from abc import ABC
from types import NoneType
from typing import Any, Generic, TypeVar, Union

from epcomms.connection.transmission import Transmission

TransmissionTypeT = TypeVar(
    "TransmissionTypeT", bound=Union[Transmission[Any, Any], NoneType]
)


class MeasurementError(Exception):
    """Custom exception for measurement-related errors."""


class CommandError(Exception):
    """Custom exception for command-related errors."""


class Instrument(ABC, Generic[TransmissionTypeT]):
    # pylint: disable=too-few-public-methods
    """
    Abstract Base Class for all Instruments.

    Instruments are software representations of agents in the real world that
    can sense the physical environment, and are the base class for all equipment.
    """

    transmission: TransmissionTypeT

    def __init__(self, transmission: TransmissionTypeT) -> None:
        self.transmission = transmission

    def close(self) -> None:
        """
        Safely close the instrument
        """
        if self.transmission is not None:
            self.transmission.close()
