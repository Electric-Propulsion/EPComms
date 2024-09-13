from abc import ABC, abstractmethod
from typing import Union


class Packet(ABC):
    """Abstract base class for packets. The represent data that's being
    transmitted, but may not map exactly to the bits on the line."""

    _data: Union[str, int, float] = None

    @abstractmethod
    def serialize_bytes(self) -> bytes:
        """Serialize the packet into bytes for transmission."""
        raise NotImplementedError("Calling abstract method!")

    @abstractmethod
    def serialize_str(self) -> str:
        """Serialize the packet into a string for transmission."""
        raise NotImplementedError("Calling abstract method!")

    @property
    def data(self) -> Union[str, int, float]:
        """Serialize the packet into a string for transmission."""
        return self._data
