from .packet import ReceivedPacket, TransmittedPacket


class ASCII(TransmittedPacket[str, bytes], ReceivedPacket[str, bytes]):
    """ASCII packets are simple strings that are sent and received as-is."""

    def __init__(self, data: str) -> None:
        self._data = data

    def serialize(self) -> bytes:
        return self._data.encode("ascii")

    @classmethod
    def from_data(cls, data: str) -> "ASCII":
        return cls(data)

    @classmethod
    def from_wire(cls, wire: bytes) -> "ASCII":
        return cls(wire.decode("ascii"))

    def deserialize(self) -> str:
        return self._data
