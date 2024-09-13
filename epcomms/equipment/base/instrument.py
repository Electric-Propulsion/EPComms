from abc import ABC
from epcomms.connection.transmission import Transmission


class Instrument(ABC):
    """
    Abstract Base Class for all Instruments.

    Instruments are software representations of agents in the real world that
    can sense the physical environment.
    """

    transmission: Transmission

    def __init__(self, transmission: Transmission):
        self.transmission = transmission
