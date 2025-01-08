"""
KeysightEDU36311A Power Supply Control
This module provides an interface to control the Keysight EDU36311A power supply.
"""

from epcomms.connection.transmission import Visa
from epcomms.connection.packet import ASCII
from . import PowerSupply


class KeysightEDU36311A(PowerSupply):
    """
    A class to represent the Keysight EDU36311A power supply.
    Attributes
    ----------
    transmission : Visa
        An instance of the Visa class for communication with the power supply.
    Methods
    -------
    __init__(resource_name: str) -> None
        Initializes the power supply with the given resource name.
    beep() -> None
        Triggers the power supply to emit a beep sound.
    set_voltage(voltage: float, channel: int = 0) -> None
        Sets the output voltage for the specified channel.
    measure_voltage(channel: int = 0) -> float
        Measures and returns the output voltage for the specified channel.
    set_current(current: float, channel: int = 0) -> None
        Sets the output current for the specified channel.
    measure_current(channel: int = 0) -> float
        Measures and returns the output current for the specified channel.
    enable_output(channel: int = 0) -> None
        Enables the output for the specified channel.
    disable_output(channel: int = 0) -> None
        Disables the output for the specified channel.
    """

    def __init__(self, resource_name) -> None:
        """
        Initializes the Keysight EDU36311A power supply.

        Args:
            resource_name (str): The VISA resource name of the power supply.
        """
        transmission = Visa(resource_name)
        super().__init__(transmission)

    def beep(self) -> None:
        """
        Sends a command to the power supply to emit a beep sound.

        This method uses the transmission interface to send the "SYST:BEEP"
        command to the connected Keysight EDU36311A power supply, causing it
        to produce an audible beep.

        Returns:
            None
        """
        self.transmission.command(ASCII("SYST:BEEP"))

    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        """
        Sets the voltage for a specified channel on the Keysight EDU36311A power supply.

        Args:
            voltage (float): The desired voltage to set.
            channel (int, optional): The channel number to set the voltage on. Defaults to 0.

        Returns:
            None
        """
        self.transmission.command(ASCII(f":INST:NSEL {channel}"))
        self.transmission.command(ASCII(f":SOUR:VOLT:LEV:IMM:AMPL {voltage}"))

    def measure_voltage_setpoint(self, channel: int = 0) -> float:
        """
        Measures the voltage on the specified channel of the Keysight EDU36311A power supply.

        Args:
            channel (int): The channel number to measure the voltage from. Default is 0.

        Returns:
            float: The measured voltage value.
        """
        self.transmission.command(ASCII(f":INST:NSEL {channel}"))
        return float(self.transmission.poll(ASCII("SOUR:VOLT:LEV:IMM:AMPL?")).data)

    def measure_voltage(self, channel: int = 0) -> float:
        """
        Measures the voltage on the specified channel of the Keysight EDU36311A power supply.

        Args:
            channel (int): The channel number to measure the voltage from. Default is 0.

        Returns:
            float: The measured voltage value.
        """
        return float(self.transmission.poll(ASCII(f":MEAS:SCAL:VOLT:DC? CH{channel}")).data)

    def set_current_limit(self, current: float, channel: int = 0) -> None:
        """
        Sets the current for a specified channel on the Keysight EDU36311A power supply.

        Args:
            current (float): The desired current value to set.
            channel (int, optional): The channel number to set the current on. Defaults to 0.

        Returns:
            None
        """
        self.transmission.command(ASCII(f":INST:NSEL {channel}"))
        self.transmission.command(ASCII(f":SOUR:CURR:LEV:IMM:AMPL {current}"))

    def measure_current_limit(self, channel: int = 0) -> float:
        """
        Measures the current from the specified channel of the power supply.

        Args:
            channel (int): The channel number to measure the current from. Default is 0.

        Returns:
            float: The measured current in amperes.
        """
        self.transmission.command(ASCII(f":INST:NSEL {channel}"))
        return float(self.transmission.poll(ASCII(":SOUR:CURR:LEV:IMM:AMPL?")).data)

    def measure_current(self, channel: int = 0) -> float:
        """
        Measures the current from the specified channel of the power supply.

        Args:
            channel (int): The channel number to measure the current from. Default is 0.

        Returns:
            float: The measured current in amperes.
        """
        return float(self.transmission.poll(ASCII(f":MEAS:SCAL:CURR:DC? CH{channel}")).data)
    
    def get_output(self, channel: int = 0) -> None:
        self.transmission.command(ASCII(f":INST:NSEL {channel}"))
        return float(self.transmission.poll(ASCII(":OUTPut:STATe?")).data)


    def set_output(self, boolean, channel: int = 0) -> None:
        """
        Enables the output for the specified channel on the Keysight EDU36311A power supply.

        Args:
            channel (int, optional): The channel number to enable output for. Defaults to 0.
        """

        value = 1 if boolean else 0

        self.transmission.command(ASCII(f":INST:NSEL {channel}"))
        self.transmission.command(ASCII(f":OUTPut:STATe {value}"))
