import logging
from dataclasses import dataclass
from threading import Thread, Lock
from typing import Callable, Literal
from concurrent.futures import Future

from epcomms.connection.packet.bytes import Bytes
from epcomms.connection.transmission import Serial, TransmissionError

from . import VacuumController

logger = logging.getLogger(__name__)


@dataclass
class InficonBGP400State:
    pressure: float | None
    unit: Literal["mbar", "Torr", "Pa", None]
    emission: Literal["Off", "25 uA", "5 mA", "Degas"]
    adjustment: str | None
    software_version: str
    toggle_bit: int
    error_msg: str | None


class InficonBGP400(VacuumController[Serial[Bytes]]):

    def __init__(self, device_location: str):
        transmission = Serial(device_location, packet_type=Bytes, frame_prefix=b'\x07\x05', frame_length=7, frame_terminator=b'')
        self._subscribers: list[Callable[[InficonBGP400State], None]] = []
        self._subscriber_lock = Lock()
        super().__init__(transmission)
        self._worker_thread = Thread(target=self.read_loop, daemon=True)
        self._worker_thread.start()

    def register_subscriber(
        self, callback: Callable[[InficonBGP400State], None]
    ) -> Callable[[], None]:
        with self._subscriber_lock:
            self._subscribers.append(callback)

        def unregister() -> None:
            with self._subscriber_lock:
                self._subscribers.remove(callback)

        return unregister

    def register_singleshot(
        self, callback: Callable[[InficonBGP400State], None]
    ) -> None:

        def self_unregistering_wrapper(state: InficonBGP400State) -> None:
            try:
                callback(state)
            finally:
                unregister()

        unregister = self.register_subscriber(self_unregistering_wrapper)

    def degass_on(self) -> None:
        packet = Bytes(bytearray([3, 16, 93, 148, 1]))
        self.transmission.command(packet)

    def degass_off(self) -> None:
        packet = Bytes(bytearray([3, 16, 93, 105, 214]))
        self.transmission.command(packet)

    def set_mbar(self) -> None:
        packet = Bytes(bytearray([3, 16, 62, 0, 78]))
        self.transmission.command(packet)

    def set_torr(self) -> None:
        packet = Bytes(bytearray([3, 16, 62, 1, 79]))
        self.transmission.command(packet)

    def set_pa(self) -> None:
        packet = Bytes(bytearray([3, 16, 62, 2, 80]))
        self.transmission.command(packet)

    def read_loop(self) -> None:
        while True:
            packet = self.transmission.read()
            data = packet.deserialize()
            try:
                state = self.decode_output_packet(data)
            except TransmissionError as e:
                print(f"Error decoding Inficon BGP400 packet: {e}")
                continue
            
            with self._subscriber_lock:
                subscriber_functions = list(self._subscribers)
            for subscriber in subscriber_functions:
                subscriber(state)

    def get_state(self) -> InficonBGP400State:
        future_state = Future[InficonBGP400State]()
        def callback(state: InficonBGP400State) -> None:
            future_state.set_result(state)

        self.register_singleshot(callback)
        return future_state.result()

    def decode_output_packet(self, packet: bytearray) -> InficonBGP400State:
        status = packet[0]
        error = packet[1]
        measurement_MSB = packet[2]
        measurement_LSB = packet[3]
        software_version = packet[4]
        sensor_type = packet[5]
        checksum = packet[6]

        if sensor_type != 10:
            raise TransmissionError(f"Invalid sensor type: {sensor_type} (expected 10)")
        if checksum != ((sum(packet[0:6])+5) % 256):
            raise TransmissionError(
                f"Invalid checksum: {checksum} (expected {(sum(packet[0:6])+5) % 256})"
            )

        emission_status = (status) & 0b11
        match emission_status:
            case 0b00:
                emission = "Off"
            case 0b01:
                emission = "25 uA"
            case 0b10:
                emission = "5 mA"
            case 0b11:
                emission = "Degas"
            case _:
                raise TransmissionError(f"Invalid emission status: {emission_status}")

        adjustment_status = (status >> 2) & 0b1
        match adjustment_status:
            case 0b00:
                adjustment = "1000 mbar adjustment off"
            case 0b01:
                adjustment = "1000 mbar adjustment on"
            case _:
                adjustment = None

        toggle_bit = (status >> 3) & 0b1

        pressure_unit = (status >> 4) & 0b11
        match pressure_unit:
            case 0b00:
                unit = "mbar"
            case 0b01:
                unit = "Torr"
            case 0b10:
                unit = "Pa"
            case _:
                unit = None

        match ((error >> 4) & 0b1111):
            case 0b0101:
                error_msg = "Pirani adjusted poorly"
            case 0b1001:
                error_msg = "BA error"
            case 0b1001:
                error_msg = "Pirani error"
            case _:
                error_msg = None

        software_version_str = f"v{software_version/20.0}"

        match unit:
            case "mbar":
                pressure = 10 ** (
                    ((measurement_MSB * 256) + measurement_LSB) / 4000 - 12.5
                )
            case "Torr":
                pressure = 10 ** (
                    ((measurement_MSB * 256) + measurement_LSB) / 4000 - 12.625
                )
            case "Pa":
                pressure = 10 ** (
                    ((measurement_MSB * 256) + measurement_LSB) / 4000 - 10.5
                )
            case _:
                pressure = None

        return InficonBGP400State(
            pressure=pressure,
            unit=unit,
            emission=emission,
            adjustment=adjustment,
            software_version=software_version_str,
            toggle_bit=toggle_bit,
            error_msg=error_msg,
        )
