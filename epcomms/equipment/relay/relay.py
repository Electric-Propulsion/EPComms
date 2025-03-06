from abc import abstractmethod
from enum import Enum
from epcomms.equipment.base import Instrument

class Relay(Instrument):
    """Abstract Base Class for all Rel
    ays."""

    class State(Enum):
        OPEN = 0
        CLOSED = 1

    @abstractmethod
    def set_state(self, state: State) -> None:
        raise NotImplementedError
    
