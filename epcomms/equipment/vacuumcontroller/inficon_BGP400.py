from typing import Union, Literal

from . import VacuumController
from epcomms.connection.packet import Bytes
from epcomms.connection.transmission import ByteSerial, TransmissionError

class InficonBGP400(VacuumController):
    def __init__(self, device_location):
        transmission = ByteSerial(device_location)
        super().__init__(transmission)

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
        while(True):
            packet = self.transmission.read()
            data = packet.as_ints()
            self.decode_output_packet(data)

    def decode_output_packet(self, packet: list[int]) -> None:
        length = packet[0]
        page = packet[1]
        status = packet[2]
        error = packet[3]
        measurement_MSB = packet[4]
        measurement_LSB = packet[5]
        software_version = packet[6]
        sensor_type = packet[7]
        checksum = packet[8]

        if length != 7:
            raise TransmissionError(f"Invalid data length: {length} (expected 7)")
        if page != 5:
            raise TransmissionError(f"Invalid page number: {page} (expected 5)")
        if sensor_type != 10:
            raise TransmissionError(f"Invalid sensor type: {sensor_type} (expected 10)")
        if checksum != (sum(packet[1:8]) % 256):
            raise TransmissionError(f"Invalid checksum: {checksum} (expected {(sum(packet[1:8]) % 256)})")

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

        adjustment_status = (status >> 2) & 0b1
        match adjustment_status:
            case 0b00:
                adjustment = "1000 mbar adjustment off"
            case 0b01:
                adjustment = "1000 mbar adjustment on"
            case _:
                adjustment = "Unknown adjustment status"

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
                unit = "Unknown"

        match ((error>>4) & 0b1111):
            case 0b0101:
                error_msg = "Pirani adjusted poorly"
            case 0b1001:
                error_msg = "BA error"
            case 0b1001:
                error_msg = "Pirani error"

        software_version_str = f"v{software_version/20.0}"

        match unit:
            case "mbar":
                pressure = 10**(((measurement_MSB * 256) + measurement_LSB) / 4000-12.5)
            case "Torr":
                pressure = 10**(((measurement_MSB * 256) + measurement_LSB) / 4000-12.625)
            case "Pa":
                pressure = 10**(((measurement_MSB * 256) + measurement_LSB) / 4000-10.5)
            case _:
                pressure = -1.0

        print(f"Pressure: {pressure} {unit}, Emission: {emission}, Adjustment: {adjustment}, Software Version: {software_version}, toggle: {toggle_bit}, Error: {error_msg if error!=0 else 'None'},")


