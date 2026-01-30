"""
BK1694 Power Supply Control over ESP32
This module provides an interface to control the BK1694 power supply by sending
commands to a server hosted on an ESP32.

See https://github.com/Electric-Propulsion/BK1694_Controller.
"""

import json
from dataclasses import dataclass

from epcomms.connection.packet import String
from epcomms.connection.transmission import Socket

from .power_supply import PowerSupply


@dataclass
class BK1694Status:
    """Dataclass representing the status of the BK1694 power supply."""

    value: int
    enable: bool


class BK1694(PowerSupply[Socket]):
    """BK1694 Power Supply ESP32 interface implementation"""

    def __init__(self, ip: str):
        self.ip = ip  # Ours is "192.168.0.156"
        self.ws_url = f"ws://{self.ip}:7777"  # shouldn't hardcode port
        transmission = Socket(self.ws_url)
        super().__init__(transmission)

    def set_voltage(self, voltage: float, channel: int | list[int]) -> None:
        """Set the voltage.

        Args:
            voltage (float): For the BK1694, a float between 0 and 30 V.
                Will be accurate to the ± 0.12 V because the user-provided
                voltage is mapped to an integer between 0-255.
        """

        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for BK1694 must"
                "be set to 1 or None."
            )
        data = json.dumps(
            {"command": "setValue", "value": self._convert_voltage_to_value(voltage)}
        )
        self.transmission.poll(String.from_data(data))

    def measure_voltage_setpoint(self, channel: int | list[int] = 1) -> float:
        """Measure the voltage setpoint."""
        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for BK1694 must "
                "be set to 1 or None."
            )
        return self._convert_value_to_voltage(self._get_status().value)

    def measure_voltage(self, channel: int | list[int]) -> float:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support measuring the output voltage."
        )

    def set_current_limit(self, current: float, channel: int | list[int]) -> None:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support setting the current limit."
        )

    def measure_current_limit(self, channel: int | list[int]) -> float:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support measuring the current limit."
        )

    def measure_current(self, channel: int | list[int]) -> float:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support measuring the output current."
        )

    def get_output(self, channel: int | list[int]) -> bool:
        """Get the output status."""
        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for BK1694 must "
                "be set to 1 or None."
            )

        return self._get_status().enable

    def set_output(self, state: bool, channel: int | list[int] = 1) -> None:
        """Enables or disables the power supply.

        Args:
            state (bool): True to enable, False to disable.

        Returns:
            dict: Response from ESP32 server.
        """
        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for BK1694 must "
                "be set to 1 or None."
            )

        data = json.dumps({"command": "enable", "value": state})
        self.transmission.poll(String.from_data(data))

    def _get_status(self) -> BK1694Status:
        """Gets system status.

        Returns:
            dict: Response from ESP32 server.
        """
        data = {"command": "getStatus"}
        response = self.transmission.poll(
            String.from_data(json.dumps(data))
        ).deserialize()
        return BK1694Status(**json.loads(response))

    def _convert_value_to_voltage(self, value: int) -> float:
        """Converts the integer value to a voltage.

        Args:
            value (int): The integer value to convert.

        Returns:
            float: The voltage corresponding to the value.
        """
        return value * 30 / 255

    def _convert_voltage_to_value(self, voltage: float) -> int:
        """Converts the voltage to an integer value.

        Args:
            voltage (float): The voltage to convert.

        Returns:
            int: The integer value corresponding to the voltage.
        """
        return int(voltage * 255 / 30)
