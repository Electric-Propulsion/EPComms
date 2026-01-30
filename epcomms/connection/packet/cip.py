from dataclasses import dataclass
from typing import Optional, TypedDict, Union

from pycomm3.tag import Tag

from .cip_datatypes import DataType
from .packet import ReceivedPacket, TransmittedPacket


@dataclass
class CIPData:
    """Data structure for CIP message content"""

    class_code: int
    instance: int
    attribute: int
    data_type: Optional[Union[type[DataType], DataType]] = None
    request_data: Union[int, float, str, bytes] = b""


class CIPGenericMessageContent(TypedDict):
    """TypedDict for CIP Generic Message Content"""

    class_code: Union[int, bytes]
    instance: Union[int, bytes]
    attribute: Union[int, bytes]
    request_data: Union[int, float, str, bytes]
    data_type: Optional[Union[type[DataType], DataType]]


class CIPTX(TransmittedPacket[CIPData, CIPGenericMessageContent]):
    """Representation of a CIP (Common Industrial Protocol) packet sent from a
    controller to a device on the network."""

    def __init__(self, data: CIPData) -> None:
        self._data = data

    def serialize(self) -> CIPGenericMessageContent:
        return CIPGenericMessageContent(
            {
                "class_code": self._data.class_code,
                "instance": self._data.instance,
                "attribute": self._data.attribute,
                "request_data": (
                    self._data.data_type.encode(self._data.request_data)
                    if self._data.request_data != b""
                    and self._data.data_type is not None
                    else self._data.request_data
                ),
                "data_type": self._data.data_type,
            }
        )

    @classmethod
    def from_data(cls, data: CIPData) -> "CIPTX":
        return cls(data)


class CIPRX(ReceivedPacket[Union[str, int, float], Tag]):
    """Representation of a CIP (Common Industrial Protocol) packet received from a
    device on the network."""

    def __init__(self, tag: Tag):
        self._data = tag.value
        self._data_type = tag.type
        self._error = tag.error

    @classmethod
    def from_wire(cls, wire: Tag) -> "CIPRX":
        return cls(wire)

    def deserialize(self) -> Union[str, int, float]:
        return self._data

    @property
    def data_type(self) -> str | None:
        """Data type of returned message, for decoding"""
        return self._data_type

    @property
    def error(self) -> str | None:
        """Error message, if any"""
        return self._error
