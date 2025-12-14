"""AlicatEIP class for communication with Alicat EIP flow control devices over EthernetIP"""

from dataclasses import dataclass

from epcomms.connection.packet import CIPTX, CIPData
from epcomms.connection.packet.cip_datatypes import REAL, STRING, UDINT, UINT, WORD
from epcomms.connection.transmission import EthernetIP, TransmissionError

from .flow_controller import FlowController



@dataclass
class DeviceReadings:
    """Data class for storing device readings."""

    gas: int
    status: int
    gauge_pressure: float
    flow_temp: float
    volumetric_flow: float
    mass_flow: float
    mass_flow_setpoint: float


class AlicatEIP(FlowController[EthernetIP]):
    """AlicatEIP class for communication with Alicat devices over EthernetIP."""

    # lookup table for identity elements
    _identity_lut: dict[str, tuple[int, type]] = {
        "vendor_id": (1, UINT),
        "device_type": (2, UINT),
        "product_code": (3, UINT),
        "status": (5, WORD),
        "serial_number": (6, UDINT),
        "product_name": (7, STRING),
    }

    def __init__(self, routing_path: str):
        transmission = EthernetIP(routing_path)
        super().__init__(transmission)

    def get_pressure(self) -> float:
        return self._get_device_readings().gauge_pressure

    def get_flow_temp(self) -> float:
        """
        Retrieves the flow temperature from the device readings.

        Returns:
            float: The flow temperature value.
        """
        return self._get_device_readings().flow_temp

    def get_volumetric_flow(self) -> float:
        """
        Retrieves the volumetric flow reading from the device.

        Returns:
            float: The current volumetric flow value.
        """
        return self._get_device_readings().volumetric_flow

    def get_mass_flow(self) -> float:
        """
        Retrieve the mass flow reading from the device.

        Returns:
            float: The mass flow value obtained from the device readings.
        """
        return self._get_device_readings().mass_flow

    def get_mass_flow_setpoint(self) -> float:
        """
        Retrieves the mass flow setpoint from the device.

        Returns:
            float: The mass flow setpoint value.
        """
        return self._get_device_readings().mass_flow_setpoint

    def get_setpoint(self) -> float:
        """
        Retrieves the current setpoint value from the flow controller.

        Returns:
            float: The current setpoint value.
        """
        packet = CIPTX.from_data(
            CIPData(class_code=4, instance=100, attribute=3, data_type=REAL)
        )
        response = self.transmission.poll(packet)
        return float(response.deserialize())

    def set_setpoint(self, setpoint: float) -> None:
        """
        Sets the setpoint for the flow controller.

        Args:
            setpoint (float): The desired setpoint value to be set on the flow controller.

        Returns:
            None
        """
        packet = CIPTX.from_data(
            CIPData(
                class_code=4,
                instance=100,
                attribute=3,
                data_type=REAL,
                request_data=setpoint,
            )
        )

        self.transmission.command(packet)

    def tare_flow(self) -> None:
        """
        Tares the flow measurement of the Alicat flow controller.

        Returns:
            None
        """
        self._send_device_command(4, 2)

    def reset_totalizer(self) -> None:
        """
        Resets the totalizer of the flow controller.

        Returns:
            None
        """
        self._send_device_command(5, 0)

    def hold_valves_closed(self) -> None:
        """
        Sends a command to hold the valves closed.
        """
        self._send_device_command(6, 1)

    def hold_valves_at_current_position(self) -> None:
        """
        Holds the valves at their current position.

        Returns:
            None
        """
        self._send_device_command(6, 2)

    def release_valves(self) -> None:
        """
        Releases the valves of the flow controller.

        Returns:
            None
        """
        self._send_device_command(6, 0)

    def get_identity_string(self) -> str:
        """
        Retrieves and constructs a string that represents the identity of the device.
        Returns:
            str: A formatted string containing the product name, vendor ID, device type,
                 product code, and serial number.
        """
        vendor_id = self._get_identity_element("vendor_id")
        device_type = self._get_identity_element("device_type")
        product_code = self._get_identity_element("product_code")
        serial_number = self._get_identity_element("serial_number")
        product_name = self._get_identity_element("product_name")

        # At least on ours, the product name is missing a leading 'E'.
        # It's not a bug in this code. Probably.
        return (
            f"{product_name} (Vendor ID: {vendor_id}, Device Type: {device_type}, "
            f"Product Code: {product_code}, Serial Number: {serial_number})"
        )

    def get_status(self):
        """
        Retrieves the status of the flow controller.

        The status is represented as a dictionary with the following keys:
        - "temp_overflow": Indicates if there is a temperature overflow.
        - "temp_underflow": Indicates if there is a temperature underflow.
        - "volumetric_overflow": Indicates if there is a volumetric overflow.
        - "volumetric_underflow": Indicates if there is a volumetric underflow.
        - "mass_overflow": Indicates if there is a mass overflow.
        - "mass_underflow": Indicates if there is a mass underflow.
        - "pressure_overflow": Indicates if there is a pressure overflow.
        - "totalizer_overflow": Indicates if there is a totalizer overflow.
        - "PID_loop_hold": Indicates if the PID loop is on hold.
        - "ADC_error": Indicates if there is an ADC error.
        - "PID_exhaust": Indicates if the PID is in exhaust mode.
        - "over_pressure_limit": Indicates if the over pressure limit is reached.
        - "flow_overflow_during_totalize": Indicates if there is a flow overflow
          during totalization.
        - "measurement_aborted": Indicates if the measurement was aborted.

        Returns:
            dict: A dictionary containing the status flags.
        """
        status = self._get_identity_element("status")

        if not isinstance(status, int):
            raise TransmissionError("Status value is not an integer.")

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

    def _get_device_readings(self) -> DeviceReadings:
        """
        Retrieves device readings from the flow controller.

        Returns:
            dict: A dictionary containing the following keys:
                - "gas" (int): The gas type identifier.
                - "status" (int): The status of the device.
                - "gauge_pressure" (float): The gauge pressure reading.
                - "flow_temp" (float): The flow temperature reading.
                - "volumetric_flow" (float): The volumetric flow rate.
                - "mass_flow" (float): The mass flow rate.
                - "mass_flow_setpoint" (float): The mass flow setpoint.
        """
        packet = CIPTX.from_data(CIPData(class_code=4, instance=101, attribute=3))

        data = self.transmission.poll(packet).deserialize()
        if not isinstance(data, bytes) or isinstance(data, str):
            # str is a subclass of bytes(?), so check that first
            raise TransmissionError("Device readings response is not bytes.")

        return DeviceReadings(
            gas=UINT.decode(data[0:2]),
            status=UDINT.decode(data[2:6]),
            gauge_pressure=REAL.decode(data[6:10]),
            flow_temp=REAL.decode(data[10:14]),
            volumetric_flow=REAL.decode(data[14:18]),
            mass_flow=REAL.decode(data[18:22]),
            mass_flow_setpoint=REAL.decode(data[22:26]),
        )

    def _send_device_command(self, command_id: int, argument: int) -> None:
        """
        Sends a command to the device and verifies the response.

        Args:
            command_id (int): The ID of the command to send.
            argument (int): The argument to accompany the command.
        Raises:
            TransmissionError: If the device does not acknowledge the command correctly.
        """
        params = UINT.encode(command_id) + UINT.encode(argument)
        packet = CIPTX.from_data(
            CIPData(class_code=4, instance=102, attribute=3, request_data=params)
        )
        self.transmission.command(packet)
        check_packet = CIPTX.from_data(CIPData(class_code=4, instance=102, attribute=3))

        data = self.transmission.poll(check_packet).deserialize()
        if not isinstance(data, bytes) or isinstance(data, str):
            # str is a subclass of bytes(?), so check that explicitly.
            raise TransmissionError("Device readings response is not bytes.")
        if UINT.decode(data[0:2]) != command_id or UINT.decode(data[2:4]) != argument:
            raise TransmissionError("Device did not acknowledge command.")

    def _get_identity_element(self, element: str) -> int | str:
        """
        Retrieves the identity element specified by the given element name.
        Args:
            element (str): The name of the identity element to retrieve.
        Returns:
            Union[int, str]: The value of the requested identity element,
            which can be either an integer or a string.
        """
        packet = CIPTX.from_data(
            CIPData(
                class_code=1,
                instance=1,
                attribute=self._identity_lut[element][0],
                data_type=self._identity_lut[element][1],
            )
        )

        response = self.transmission.poll(packet)

        data = response.deserialize()
        if isinstance(data, float):
            raise TransmissionError("Received float when int or str was expected.")
        return data
