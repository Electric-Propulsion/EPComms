"""
KeysightEDU34550A Multimeter Control
This module provides an interface to control the Keysight EDU34550A multimeter.
"""

from epcomms.connection.transmission import Visa
from epcomms.connection.packet import ASCII
from typing import Union
from . import Multimeter


class KeysightEDU34450A(Multimeter):
    """
    A class to represent the Keysight EDU34450A multimeter.
    Attributes
    ----------
    transmission : Visa
        An instance of the Visa class for communication with the multimeter.
    Methods
    -------
    __init__(resource_name: str) -> None
        Initializes the multimeter with the given resource name.
    """

    def __init__(self, resource_name) -> None:
        """
        Initializes the Keysight EDU34450A multimeter.

        Args:
            resource_name (str): The VISA resource name of the multimeter.
        """
        transmission = Visa(resource_name)
        super().__init__(transmission)

    def beep(self) -> None:
        """
        Sends a command to the multimeter to emit a beep sound.

        This method uses the transmission interface to send the "SYST:BEEP"
        command to the connected Keysight EDU34450A multimeter, causing it
        to produce an audible beep.

        Returns:
            None
        """
        self.transmission.command(ASCII("SYST:BEEP"))

    def measure_voltage_ac(self, range: Union[str|int|float] = 'AUTO', resolution: Union[str|int|float] = 'DEF', channel: str = 'PRIMARY') -> float:
        """Measures AC voltage at a desired resolution using a specified range, on a specified channel.

        Args:
            range (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            channel (str, optional): Select either 'PRIMARY' or 'SECONDARY' multimeter channel. Defaults to 'PRIMARY'.

        Returns:
            float: The measured voltage value.
        """
        assert isinstance(range, float) or isinstance(range, int) or range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert isinstance(resolution, float) or isinstance(resolution, int) or range.upper in {'DEF','MAX','MIN'} 
        assert channel.upper in {'PRIMARY', 'SECONDARY'}
        range_str = range if isinstance(range, str) else f"{range:.2e}"
        resolution_str = resolution if isinstance(resolution, str) else f"{resolution:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:{channel}:VOLTAGE:AC? {range_str},{resolution_str}")))
    
    def measure_voltage_dc(self, range: Union[str|int|float] = 'AUTO', resolution: Union[str|int|float] = 'DEF', channel: str = 'PRIMARY') -> float:
        """Measures DC voltage at a desired resolution using a specified range, on a specified channel.

        Args:
            range (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            channel (str, optional): Select either 'PRIMARY' or 'SECONDARY' multimeter channel. Defaults to 'PRIMARY'.

        Returns:
            float: The measured voltage value.
        """
        assert isinstance(range, float) or isinstance(range, int) or range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert isinstance(resolution, float) or isinstance(resolution, int) or range.upper in {'DEF','MAX','MIN'} 
        assert channel.upper in {'PRIMARY', 'SECONDARY'}
        range_str = range if isinstance(range, str) else f"{range:.2e}"
        resolution_str = resolution if isinstance(resolution, str) else f"{resolution:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:{channel}:VOLTAGE:DC? {range_str},{resolution_str}")))
    
    def measure_capacitance(self, range: Union[str|int] = 'AUTO', resolution: Union[str|int] = 'DEF') -> float:
        """Measures capacitance at a desired resolution using a specified range, on the 'PRIMARY' channel.

        Args:
            range (Union[str | int | float], optional): Specify a numeric value (in Farads), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (Union[str | int | float], optional): Specify a numeric value (in Farads), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured capacitance value.
        """
        assert isinstance(range, float) or isinstance(range, int) or range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert isinstance(resolution, float) or isinstance(resolution, int) or range.upper in {'DEF','MAX','MIN'} 
        range_str = range if isinstance(range, str) else f"{range:.2e}"
        resolution_str = resolution if isinstance(resolution, str) else f"{resolution:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:CAPACITANCE? {range_str},{resolution_str}")))
    
    def measure_continuity(self) -> Union[float|str]:
        """Performs a 2-wire continuity test.

        Returns:
            float: A resistance reading, as returned by the instrument during continuity tests. 
        """
        #TODO confirm return value when instrument sees an open circuit (>1.2 kOhm). Programmer guide is unclear.
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:CONTINUITY?")))
    
    def measure_current_ac(self, range: Union[str|int|float] = 'AUTO', resolution: Union[str|int|float] = 'DEF', channel: str = 'PRIMARY') -> float:
        """Measures AC current at a desired resolution using a specified range, on a specified channel.

        Args:
            range (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            channel (str, optional): Select either 'PRIMARY' or 'SECONDARY' multimeter channel. Defaults to 'PRIMARY'.

        Returns:
            float: The measured current value.
        """
        assert isinstance(range, float) or isinstance(range, int) or range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert isinstance(resolution, float) or isinstance(resolution, int) or range.upper in {'DEF','MAX','MIN'} 
        assert channel.upper in {'PRIMARY', 'SECONDARY'}
        range_str = range if isinstance(range, str) else f"{range:.2e}"
        resolution_str = resolution if isinstance(resolution, str) else f"{resolution:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:{channel}:CURRENT:AC? {range_str},{resolution_str}")))
    
    def measure_current_dc(self, range: Union[str|int|float] = 'AUTO', resolution: Union[str|int|float] = 'DEF', channel: str = 'PRIMARY') -> float:
        """Measures DC current at a desired resolution using a specified range, on a specified channel.

        Args:
            range (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            channel (str, optional): Select either 'PRIMARY' or 'SECONDARY' multimeter channel. Defaults to 'PRIMARY'.

        Returns:
            float: The measured current value.
        """
        assert isinstance(range, float) or isinstance(range, int) or range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert isinstance(resolution, float) or isinstance(resolution, int) or range.upper in {'DEF','MAX','MIN'} 
        assert channel.upper in {'PRIMARY', 'SECONDARY'}
        range_str = range if isinstance(range, str) else f"{range:.2e}"
        resolution_str = resolution if isinstance(resolution, str) else f"{resolution:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:{channel}:CURRENT:DC? {range_str},{resolution_str}")))
    
    def measure_diode(self) -> float:
        """Performs a diode test.

        Returns:
            float: A voltage reading, as returned by the instrument during diode tests, if the voltage is in the range [0,1.2]. If the signal is greater than 1.2V then the value +9.9e+37 is returned. 
        """
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:DIODE?")))
    
    def measure_frequency(self, freq_range: Union[str|int|float] = 'DEF', freq_resolution: Union[str|int|float] = 'DEF', volt_range: Union[str|int|float] = 0.1, channel: str = 'PRIMARY') -> float:
        """Measures frequency of an AC volage signal at a desired resolution using a specified range, on a specified channel.

        Before frequency measurement, the AC voltage range is configured. As per the programmer guide, the voltage range should be "at least" 0.1V for accurate frequency measurements.

        Args:
            freq_range (Union[str | int | float], optional): Specify a numeric value (in Hz), or one of {DEF|MAX|MIN}. MIN = DEF = 1 Hz, MAX = 1 MHz. Defaults to 'DEF'.
            freq_resolution (Union[str | int | float], optional): Specify a numeric value (in Hz), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            volt_range (Union[str | int | float], optional): Specify a numeric value (in V), or one of {AUTO|DEF|MAX|MIN}. Defaults to 0.1 V.
            channel (str, optional): Select either 'PRIMARY' or 'SECONDARY' multimeter channel. Defaults to 'PRIMARY'.

        Returns:
            float: The measured current value.
        """
        assert isinstance(freq_range, float) or isinstance(freq_range, int) or freq_range.upper in {'DEF','MAX','MIN'} 
        assert isinstance(freq_resolution, float) or isinstance(freq_resolution, int) or freq_range.upper in {'DEF','MAX','MIN'} 
        assert isinstance(volt_range, float) or isinstance(volt_range, int) or volt_range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert channel.upper in {'PRIMARY', 'SECONDARY'}
        range_str = freq_range if isinstance(freq_range, str) else f"{freq_range:.2e}"
        resolution_str = freq_resolution if isinstance(freq_resolution, str) else f"{freq_resolution:.2e}"

        self.transmission.command(f"SENSE:{channel}:FREQUENCY:VOLTAGE:RANGE {volt_range}")
        return float(self.transmission.poll(ASCII(f"MEASURE:{channel}:FREQUENCY? {range_str},{resolution_str}")))
    
    def measure_resistance(self, range: Union[str|int|float] = 'AUTO', resolution: Union[str|int|float] = 'DEF') -> float:
        """Performs 2-wire resistance measurement at a desired resolution using a specified range, on the PRIMARY channel.

        Args:
            range (Union[str | int | float], optional): Specify a numeric value (in Ohms), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (Union[str | int | float], optional): Specify a numeric value (in Ohms), or one of {DEF|MAX|MIN}. If using autoranging (range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured resistance value.
        """
        assert isinstance(range, float) or isinstance(range, int) or range.upper in {'AUTO','DEF','MAX','MIN'} 
        assert isinstance(resolution, float) or isinstance(resolution, int) or range.upper in {'DEF','MAX','MIN'} 
        range_str = range if isinstance(range, str) else f"{range:.2e}"
        resolution_str = resolution if isinstance(resolution, str) else f"{resolution:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:RESISTANCE? {range_str},{resolution_str}")))
