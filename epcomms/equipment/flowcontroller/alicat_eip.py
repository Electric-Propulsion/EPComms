from typing import Union
from epcomms.connection.packet import CIPTX, CIPRX
from epcomms.connection.packet import UINT, REAL, STRING, UDINT, WORD
from epcomms.connection.transmission import EthernetIP, TransmissionError
from . import FlowController


class AlicatEIP(FlowController):
    """AlicatEIP class for communication with Alicat devices over EthernetIP"""

    # loop up table for identity elements
    identity_lut = {
        "vendor_ID": [1, UINT],
        "device_type": [2, UINT],
        "product_code": [3, UINT],
        "status": [5, WORD],
        "serial_number": [6, UDINT],
        "product_name": [7, STRING],
    }

    def __init__(self, routing_path):
        transmission = EthernetIP(routing_path)
        super().__init__(transmission)

    def get_pressure(self) -> float:
        return self._get_device_readings()["pressure"]

    def get_flow_temp(self) -> float:
        return self._get_device_readings()["flow_temp"]

    def get_volumetric_flow(self) -> float:
        return self._get_device_readings()["volumetric_flow"]

    def get_mass_flow(self) -> float:
        return self._get_device_readings()["mass_flow"]

    def get_mass_flow_setpoint(self) -> float:
        return self._get_device_readings()["mass_flow_setpoint"]

    def get_mass_total(self) -> float:
        return self._get_device_readings()["mass_total"]

    def get_setpoint(self) -> float:
        packet = CIPTX(class_code=4, instance=100, attribute=3, data_type=REAL)
        response = self.transmission.poll(packet)
        return response.data

    def set_setpoint(self, setpoint: float) -> None:
        packet = CIPTX(
            class_code=4,
            instance=100,
            attribute=3,
            data_type=REAL,
            parameters=setpoint,
        )
        self.transmission.command(packet)

    def tare_flow(self) -> None:
        self._send_device_command(4, 2)

    def reset_totalizer(self) -> None:
        self._send_device_command(5, 0)

    def hold_valves_closed(self) -> None:
        self._send_device_command(6, 1)

    def hold_valves_at_current_position(self) -> None:
        self._send_device_command(6, 2)

    def release_valves(self) -> None:
        self._send_device_command(6, 0)

    def get_identity_string(self) -> str:
        vendor_ID = self._get_identity_element("vendor_ID")
        device_type = self._get_identity_element("device_type")
        product_code = self._get_identity_element("product_code")
        serial_number = self._get_identity_element("serial_number")
        product_name = self._get_identity_element("product_name")

        # At least on ours, the product name is missing a leading 'E'.
        # It's not a bug in this code. Probably.
        return f"{product_name} (Vendor ID: {vendor_ID}, Device Type: {device_type}, Product Code: {product_code}, Serial Number: {serial_number})"

    def get_status(self):
        status = self._get_identity_element("status")
        return {
            "temp_overflow": bool(status & 0b000000000000001),
            "temp_underflow": bool(status & 0b000000000000010),
            "volumetric_overflow": bool(status & 0b000000000000100),
            "volumetric_underflow": bool(status & 0b000000000001000),
            "mass_overflow": bool(status & 0b000000000010000),
            "mass_underflow": bool(status & 0b000000000100000),
            "pressure_overflow": bool(status & 0b000000001000000),
            "totalizer_overflow": bool(status & 0b000000010000000),
            "PID_loop_hold": bool(status & 0b0000001000000000),
            "ADC_error": bool(status & 0b0000010000000000),
            "PID_exhaust": bool(status & 0b0000100000000000),
            "over_pressure_limit": bool(status & 0b0001000000000000),
            "flow_overflow_during_totalize": bool(status & 0b0010000000000000),
            "measurement_aborted": bool(status & 0b0100000000000000),
        }

    def _get_device_readings(self) -> dict:
        packet = CIPTX(
            class_code=4,
            instance=101,
            attribute=3,
        )

        data = self.transmission.poll(packet).data

        return {
            "gas": UINT.decode(data[0:2]),
            "status": UDINT.decode(data[2:6]),
            "gauge_pressure": REAL.decode(data[6:10]),
            "flow_temp": REAL.decode(data[10:14]),
            "volumetric_flow": REAL.decode(data[14:18]),
            "mass_flow": REAL.decode(data[18:22]),
            "mass_flow_setpoint": REAL.decode(data[22:26]),
        }

    def _send_device_command(self, command_id: int, argument: int) -> None:
        params = UINT.encode(command_id) + UINT.encode(argument)
        print(params)
        packet = CIPTX(class_code=4, instance=102, attribute=3, parameters=params)
        self.transmission.command(packet)

        check_packet = CIPTX(class_code=4, instance=102, attribute=3)

        response = self.transmission.poll(check_packet)

        if (
            UINT.decode(response.data[0:2]) != command_id
            or UINT.decode(response.data[2:4]) != argument
        ):
            raise TransmissionError("Device did not acknowledge command.")

    def _get_identity_element(self, element: str) -> Union[int, str]:
        packet = CIPTX(
            class_code=1,
            instance=1,
            attribute=self.identity_lut[element][0],
            data_type=self.identity_lut[element][1],
        )

        response = self.transmission.poll(packet)

        return response.data
