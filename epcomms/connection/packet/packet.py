from typing import Protocol, TypeVar

Data = TypeVar("Data", infer_variance=True)
Wire = TypeVar("Wire", infer_variance=True)


class TransmittedPacket(
    Protocol[Data, Wire],
):
    def serialize(self) -> Wire: ...

    @classmethod
    def from_data(cls, data: Data) -> "TransmittedPacket[Data, Wire]": ...


class ReceivedPacket(Protocol[Data, Wire]):
    @classmethod
    def from_wire(cls, wire: Wire) -> "ReceivedPacket[Data, Wire]": ...

    def deserialize(self) -> Data: ...
