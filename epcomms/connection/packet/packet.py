from typing import Protocol, TypeVar

Data = TypeVar("Data", infer_variance=True)
Wire = TypeVar("Wire", infer_variance=True)


class TransmittedPacket(
    Protocol[Data, Wire],
):
    """Base protocol for transmitted packets."""

    def serialize(self) -> Wire:
        """Serialize a packet for transmission over the wire

        Returns:
            Wire: The wire-ready representation of the data.
        """
        ...

    @classmethod
    def from_data(cls, data: Data) -> "TransmittedPacket[Data, Wire]":
        """Create a transmitted packet from data.

        Args:
            data (Data): The data to be transmitted.
        Returns:
            TransmittedPacket[Data, Wire]: The transmitted packet instance.
        """
        ...


class ReceivedPacket(Protocol[Data, Wire]):
    """Base protocol for received packets."""

    @classmethod
    def from_wire(cls, wire: Wire) -> "ReceivedPacket[Data, Wire]":
        """Create a packet from received data

        Args:
            wire (Wire): data received from the wire.

        Returns:
            ReceivedPacket[Data, Wire]: The received packet instance.
        """
        ...

    def deserialize(self) -> Data:
        """Deserialize a packet to access it's data

        Returns:
            Data: The deserialized data.
        """
        ...
