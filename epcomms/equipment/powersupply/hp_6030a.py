"""
HP 6030A Power Supply Control
This module provides an interface to control the HP 6030AA power supply.
"""

from typing import Literal, Union

from epcomms.connection.packet import String
from epcomms.connection.transmission import Visa
from epcomms.equipment.base import SCPIInstrument

from . import PowerSupply

# TODO: still unhappy with channel handling here


class HP6030A(PowerSupply[Visa], SCPIInstrument):
    """
    A class to represent the HP6030A power supply.
    """

    def __init__(self, resource_name: str) -> None:
        """
        Initializes the HP6030A power supply.

        Args:
            resource_name (str): The VISA resource name of the power supply.
        """
        transmission = Visa(resource_name)
        super().__init__(transmission)

    def set_language(self, language: Literal["TMSL", "COMP"] = "TMSL") -> None:
        """
        Sets the language used to communicate with the power supply.

        Args:
            language (Literal): COMP (compatability) or TMSL (SCPI commands)
        Returns:
            None
        """
        self.transmission.command(
            String.from_data(self.generate_command("SYST:LANG", arguments=language))
        )

    def set_voltage(self, voltage: float, channel: Union[int, list[int]] = 1) -> None:
        """
        Sets the voltage for a specified channel on the HP6030A power supply.

        Args:
            voltage (float): The desired voltage to set.
            channel (int, optional): The channel number to set the voltage on.

        Returns:
            None
        """
        if channel not in [None, 1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        self.transmission.command(
            String.from_data(self.generate_command("VOLT", arguments=str(voltage)))
        )

    def measure_voltage_setpoint(
        self, channel: Union[int, list[int]] = 1
    ) -> float | list[float]:
        """
        Measures the voltage on the specified channel of the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the voltage from.

        Returns:
            float: The measured voltage value.
        """
        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        return self.parse_response(
            float,
            self.transmission.poll(
                String.from_data(self.generate_query("VOLT", channels=None))
            ).deserialize(),
        )

    def measure_voltage(
        self, channel: Union[int, list[int]] = 1
    ) -> float | list[float]:
        """
        Measures the voltage on the specified channel of the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the voltage from.

        Returns:
            float: The measured voltage value.
        """
        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        return self.parse_response(
            float,
            self.transmission.poll(
                String.from_data(self.generate_query("MEAS:VOLT", channels=None))
            ).deserialize(),
        )

    def set_current_limit(
        self, current: float, channel: Union[int, list[int]] = 1
    ) -> None:
        """
        Sets the current for a specified channel on the HP6030A power supply.

        Args:
            current (float): The desired current value to set.
            channel (int, optional): The channel number to set the current on.

        Returns:
            None
        """
        if channel not in [1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        self.transmission.command(
            String.from_data(self.generate_command("CURR", arguments=str(current)))
        )

    def measure_current_limit(
        self, channel: Union[int, list[int]] = 1
    ) -> float | list[float]:
        """
        Measures the current from the specified channel of the power supply.

        Args:
            channel (int): The channel number to measure the current from.

        Returns:
            float: The measured current in amperes.
        """
        if channel not in [None, 1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        return self.parse_response(
            float,
            self.transmission.poll(
                String.from_data(self.generate_query("CURR"))
            ).deserialize(),
        )

    def measure_current(
        self, channel: Union[int, list[int]] = 1
    ) -> float | list[float]:
        """
        Measures the current from the specified channel of the power supply.

        Args:
            channel (int): The channel number to measure the current from.

        Returns:
            float: The measured current in amperes.
        """
        if channel not in [None, 1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        return self.parse_response(
            float,
            self.transmission.poll(
                String.from_data(self.generate_query("MEAS:CURR", channels=None))
            ).deserialize(),
        )

    def get_output(self, channel: Union[int, list[int]] = 1) -> bool | list[bool]:
        """
        Measures the output status of the specified channel on the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the output status from.

        Returns:
            bool: The output status of the channel.
        """
        if channel not in [None, 1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        return self.parse_response(
            lambda value: bool(int(value)),
            self.transmission.poll(
                String.from_data(self.generate_query("OUTP", channels=None))
            ).deserialize(),
        )

    def set_output(self, state: bool, channel: Union[int, list[int]] = 1) -> None:
        """
        Enables the output for the specified channel on the HP6030A power supply.

        Args:
            channel (int, optional): The channel number to enable output for.
        """
        if channel not in [None, 1, [1]]:
            raise ValueError(
                f"Invalid channel provided: {channel}. Channel for HP 6030A must be set to 1 or None."
            )

        value = 1 if state else 0
        self.transmission.command(
            String.from_data(self.generate_command("OUTP", arguments=str(value)))
        )
