from . import Packet

class Bytes(Packet):
    """Bytes packet class
    Bytes packets are raw byte sequences ."""

    def __init__(self, data: bytearray) -> None:
        self._data = data

    def serialize_str(self) -> str:
        raise NotImplementedError("Cannot serialize bytes to str")

    def serialize_bytes(self) -> bytearray:
        return bytes(self._data)
    
    def as_ints(self) -> list[int]:
        """Return the byte data as a list of integers."""
        return list(self._data)
    
