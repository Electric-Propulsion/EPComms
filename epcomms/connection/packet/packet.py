from abc import ABC, abstractmethod
from typing import Union


class Packet(ABC):
    """Abstract base class for packets"""

    @abstractmethod
    def serialize_bytes(self) -> bytes:
        """Serialize the packet into bytes for transmission."""
        raise NotImplementedError("Calling abstract method!")

    @abstractmethod
    def serialize_str(self) -> str:
        """Serialize the packet into a string for transmission."""
        raise NotImplementedError("Calling abstract method!")
