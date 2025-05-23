"""ASCII packet class"""

from . import Packet


class ASCII(Packet):
    """ASCII packet class
    ASCII packets are simple strings that are sent and received as-is."""

    def __init__(self, data: str) -> None:
        self._data = data

    def serialize_str(self) -> str:
        return f"{self._data}"

    def serialize_bytes(self) -> bytes:
        return self._data.encode("ascii")
