"""
HP 6030A Power Supply Control
This module provides an interface to control the HP 6030AA power supply.
"""

from typing import Union
from epcomms.connection.transmission import Visa
from epcomms.connection.packet import ASCII
from epcomms.equipment.base import SCPIInstrument
from . import PowerSupply


class HP6030A(PowerSupply, SCPIInstrument):
    """
    A class to represent the HP6030A power supply.
    """

    def __init__(self, resource_name) -> None:
        """
        Initializes the HP6030A power supply.

        Args:
            resource_name (str): The VISA resource name of the power supply.
        """
        transmission = Visa(resource_name)
        super().__init__(transmission)

    def get_language(self) -> float:
        """
        Measures the voltage on the specified channel of the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the voltage from.

        Returns:
            float: The measured voltage value.
        """
        return self.parse_response(float,
            self.transmission.poll(ASCII(self.generate_query("SYST:LANG"))).data
        )
    
    def set_language(self, language: str = 'TMSL') -> None:
        """
        Sets the voltage for a specified channel on the HP6030A power supply.

        Args:
            voltage (float): The desired voltage to set.
            channel (int, optional): The channel number to set the voltage on.

        Returns:
            None
        """
        self.transmission.command(
            ASCII(self.generate_command("SYST:LANG", arguments=language))
        )

    def set_voltage(self, voltage: float, channel: Union[int, list[int]]) -> None:
        """
        Sets the voltage for a specified channel on the HP6030A power supply.

        Args:
            voltage (float): The desired voltage to set.
            channel (int, optional): The channel number to set the voltage on.

        Returns:
            None
        """
        self.transmission.command(
            ASCII(self.generate_command("VOLT", arguments=str(voltage), channels=None))
        )

    def measure_voltage_setpoint(self, channel: Union[int, list[int]]) -> float:
        """
        Measures the voltage on the specified channel of the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the voltage from.

        Returns:
            float: The measured voltage value.
        """
        return self.parse_response(float,
            self.transmission.poll(ASCII(self.generate_query("VOLT", channels=None))).data
        )

    def measure_voltage(self, channel: Union[int, list[int]]) -> float:
        """
        Measures the voltage on the specified channel of the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the voltage from.

        Returns:
            float: The measured voltage value.
        """
        return self.parse_response(float,
            self.transmission.poll(
                ASCII(self.generate_query("MEAS:VOLT", channels=None))
            ).data
        )

    def set_current_limit(self, current: float, channel: Union[int, list[int]]) -> None:
        """
        Sets the current for a specified channel on the HP6030A power supply.

        Args:
            current (float): The desired current value to set.
            channel (int, optional): The channel number to set the current on.

        Returns:
            None
        """
        self.transmission.command(
            ASCII(self.generate_command("CURR", arguments=str(current), channels=None))
        )

    def measure_current_limit(self, channel: Union[int, list[int]]) -> float:
        """
        Measures the current from the specified channel of the power supply.

        Args:
            channel (int): The channel number to measure the current from.

        Returns:
            float: The measured current in amperes.
        """
        return self.parse_response(float,
            self.transmission.poll(ASCII(self.generate_query("CURR", channels=None))).data
        )

    def measure_current(self, channel: Union[int, list[int]]) -> float:
        """
        Measures the current from the specified channel of the power supply.

        Args:
            channel (int): The channel number to measure the current from.

        Returns:
            float: The measured current in amperes.
        """
        return self.parse_response(float,
            self.transmission.poll(
                ASCII(self.generate_query("MEAS:CURR", channels=None))
            ).data
        )

    def get_output(self, channel: Union[int, list[int]]) -> bool:
        """
        Measures the output status of the specified channel on the HP6030A power supply.

        Args:
            channel (int): The channel number to measure the output status from.

        Returns:
            bool: The output status of the channel.
        """
        return self.parse_response(lambda value: bool(int(value)), 
            self.transmission.poll(ASCII(self.generate_query("OUTP", channels=None))).data
        )

    def set_output(self, state: bool, channel: Union[int, list[int]]) -> None:
        """
        Enables the output for the specified channel on the HP6030A power supply.

        Args:
            channel (int, optional): The channel number to enable output for.
        """
        value = 1 if state else 0
        self.transmission.command(
            ASCII(self.generate_command("OUTP", arguments=str(value), channels=None))
        )
