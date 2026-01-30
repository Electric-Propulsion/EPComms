from .packet import ReceivedPacket, TransmittedPacket


class Bytes(
    ReceivedPacket[bytearray, bytes],
    TransmittedPacket[bytearray, bytes],
):
    """
    Bytes packets are raw byte sequences.
    """

    def __init__(self, data: bytes) -> None:
        self._data = data

    def serialize(self) -> bytes:
        return self._data

    @classmethod
    def from_data(cls, data: bytearray) -> "Bytes":
        return cls(bytes(data))

    @classmethod
    def from_wire(cls, wire: bytes) -> "Bytes":
        return cls(wire)

    def deserialize(self) -> bytearray:
        return bytearray(self._data)
