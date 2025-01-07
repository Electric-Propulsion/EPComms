"""
This module defines the Instrument class, which serves as an abstract base class
for all instruments that can sense the physical environment.
"""

from abc import ABC, abstractmethod
from epcomms.connection.transmission import Transmission

class MeasurementError(Exception):
    pass

class CommandError(Exception):
    pass


class Instrument(ABC):
    # pylint: disable=too-few-public-methods
    """
    Abstract Base Class for all Instruments.

    Instruments are software representations of agents in the real world that
    can sense the physical environment.
    """

    transmission: Transmission

    def __init__(self, transmission: Transmission):
        self.transmission = transmission

    def close(self) -> None:
        self.transmission.close()