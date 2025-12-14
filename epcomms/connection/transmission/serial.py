from typing import TypeVar

from serial import Serial as Pyserial

from epcomms.connection.packet import ASCII, Bytes

from .transmission import Transmission

T = TypeVar("T", ASCII, Bytes)


class Serial(Transmission[T, T]):

    def __init__(
        self,
        device: str,
        baud: int = 9600,
        frame_terminator: bytes = b"\r\n",
        frame_prefix: bytes = b"",
        frame_length: (
            int | None
        ) = None,  # number of bytes to read after prefix and before terminator
        packet_type: type[T] = ASCII,
    ):
        self.driver = Pyserial(device, baud)
        self._packet_type = packet_type
        self._frame_terminator = frame_terminator
        self._frame_prefix = frame_prefix
        self._frame_length = frame_length
        super().__init__()

        if frame_length is None and frame_terminator == b"":
            raise ValueError(
                "At least one of frame_length or frame_terminator must be specified"
            )
        

    def _command(self, packet: T) -> None:
        self.driver.write(packet.serialize())

    def _read(self) -> T:
        data = bytes()
        self.driver.read_until(self._frame_prefix)
        if self._frame_length is not None:
            data += self.driver.read(self._frame_length)
            postfix = self.driver.read(len(self._frame_terminator))
            if postfix != self._frame_terminator:
                raise RuntimeError("Frame terminator not found where expected")
        else:
            data += self.driver.read_until(self._frame_terminator)[
                : -len(self._frame_terminator)
            ]

        return self._packet_type.from_wire(data)
