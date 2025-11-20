"""
This module defines the Instrument class, which serves as an abstract base class
for all instruments that can sense the physical environment.
"""

from abc import ABC
from types import NoneType
from typing import Any, Generic, TypeVar, Union

from epcomms.connection.transmission import Transmission

TransmissionType = TypeVar(
    "TransmissionType", bound=Union[Transmission[Any, Any], NoneType]
)


class MeasurementError(Exception):
    pass


class CommandError(Exception):
    pass


class Instrument(ABC, Generic[TransmissionType]):
    # pylint: disable=too-few-public-methods
    """
    Abstract Base Class for all Instruments.

    Instruments are software representations of agents in the real world that
    can sense the physical environment.
    """

    transmission: TransmissionType

    def __init__(self, transmission: TransmissionType) -> None:
        self.transmission = transmission

    def close(self) -> None:
        if self.transmission is not None:
            self.transmission.close()
