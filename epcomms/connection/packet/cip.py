from . import Packet
from . import DataType
from typing import Union
from pycomm3 import Tag


class CIPTX(Packet):
    """CIP Tx packet class
    Representation of a CIP (Common Industrial Protocol) packet sent from a
    controller to a device on the network."""

    def __init__(
        self,
        class_code: int,
        instance: int,
        attribute: int,
        parameters: Union[int, float, str, bytes] = b"",
        data_type: Union[DataType, None] = None,
    ) -> None:
        self._class_code = class_code
        self._instance = instance
        self._attribute = attribute
        self._data_type = data_type
        if parameters != b"" and self.data_type is not None:
            self._parameters = self._data_type.encode(parameters)
        else:
            self._parameters = parameters
        self._data = {
            "class_code": self._class_code,
            "attribute": self._attribute,
            "parameters": self._parameters,
            "data_type": self._data_type,
        }

    @property
    def class_code(self) -> int:
        return self._class_code

    @property
    def instance(self) -> int:
        return self._instance

    @property
    def attribute(self) -> int:
        return self._attribute

    @property
    def parameters(self) -> Union[list, None]:
        return self._parameters

    @property
    def data_type(self) -> Union[DataType, None]:
        return self._data_type

    def serialize_str(self) -> str:
        raise NotImplementedError("CIP TX packets cannot be serialized to strings.")

    def serialize_bytes(self) -> bytes:
        raise NotImplementedError("CIP TX packets cannot be serialized to bytes.")


class CIPRX(Packet):
    """CIP Rx packet class
    Representation of a CIP (Common Industrial Protocol) packet received from a
    device on the network."""

    def __init__(self, tag: Tag):
        self._data = tag.value
        self._data_type = tag.type
        self._error = tag.error

    @property
    def data(self) -> Union[str, int, float]:
        return self._data

    @property
    def data_type(self) -> DataType:
        return self._data_type

    @property
    def error(self) -> str:
        return self._error

    def serialize_str(self) -> str:
        raise NotImplementedError("CIP RX packets cannot be serialized to strings.")

    def serialize_bytes(self) -> bytes:
        raise NotImplementedError("CIP RX packets cannot be serialized to bytes.")
