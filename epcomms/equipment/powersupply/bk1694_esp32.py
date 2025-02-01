"""
BK1694 Power Supply Control over ESP32
This module provides an interface to control the BK1694 power supply by sending commands to a server hosted on an ESP32.
See https://github.com/Electric-Propulsion/BK1694_Controller.
"""

from epcomms.connection.transmission.sockets import Socket
from . import PowerSupply


class BK1694(PowerSupply):

    def __init__(self, ip: str):
        self.ip = ip  # Ours is "192.168.0.156"
        self.ws_url = f"ws://{self.ip}:7777"  # shouldn't hardcode port
        self.socket = Socket(self.ws_url)

    def set_voltage(self, voltage: float) -> dict:
        """Set the voltage.

        Args:
            voltage (float): For the BK1694, a float between 0 and 30 V.
                Will be accurate to the ± 0.12 V because the user-provided
                voltage is mapped to an integer between 0-255.
        """
        data = {"command": "setValue", "value": int(voltage * 255 / 30)}
        self.socket.poll(data)

    def measure_voltage_setpoint(self):
        """Measure the voltage setpoint."""
        return self._convert_value_to_voltage(self._get_status()["value"])

    def measure_voltage(self):
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support measuring the output voltage."
        )

    def set_current_limit(self, current: float) -> None:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support setting the current limit."
        )

    def measure_current_limit(self) -> None:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support measuring the current limit."
        )

    def measure_current(self) -> None:
        """Not implemented."""
        raise NotImplementedError(
            "The BK1694 does not support measuring the output current."
        )

    def get_output(self) -> None:
        """Get the output status."""
        return self._get_status()["enable"]

    def set_output(self, state: bool) -> None:
        """Enables or disables the power supply.

        Args:
            state (bool): True to enable, False to disable.

        Returns:
            dict: Response from ESP32 server.
        """
        data = {"command": "enable", "value": state}
        self.socket.poll(data)

    def _get_status(self) -> dict:
        """Gets system status.

        Returns:
            dict: Response from ESP32 server.
        """
        data = {"command": "getStatus"}
        response = self.socket.poll(data)
        return response

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
