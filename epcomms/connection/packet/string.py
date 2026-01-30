from .packet import ReceivedPacket, TransmittedPacket


class String(TransmittedPacket[str, str], ReceivedPacket[str, str]):
    """String packets are simple strings that are sent and received as-is.
    Unlike ASCII packets, they are not encoded to bytes - this is useful for
    protocols that transmit string data directly.
    """

    def __init__(self, data: str) -> None:
        self._data = data

    def serialize(self) -> str:
        return self._data

    @classmethod
    def from_data(cls, data: str) -> "String":
        return cls(data)

    @classmethod
    def from_wire(cls, wire: str) -> "String":
        return cls(wire)

    def deserialize(self) -> str:
        return self._data
