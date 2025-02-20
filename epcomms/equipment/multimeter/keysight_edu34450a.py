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

    def close(self) -> None:
        self.transmission.close()

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

    def measure_voltage_ac(self, measurement_range: Union[str|int|float] = 'AUTO', resolution: str = 'DEF') -> float:
        """Measures AC voltage using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            channel (str, optional): Only 'PRIMARY' channel works. Defaults to 'PRIMARY'.

        Returns:
            float: The measured voltage value.
        """

        try:
            assert isinstance(measurement_range, (float,int)) or measurement_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")
        
        try:
            assert resolution.upper() in {'DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'.")

        
        
        range_str = measurement_range if isinstance(measurement_range, str) else f"{measurement_range:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:VOLTAGE:AC? {range_str},{resolution}")).data)
    
    def measure_voltage_dc(self, measurement_range: Union[str|int|float] = 'AUTO', resolution: str = 'DEF') -> float:
        """Measures DC voltage using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured voltage value.
        """
        try:
            assert isinstance(measurement_range, (float,int)) or measurement_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")
        
        try:
            assert resolution.upper() in {'DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'.")

        
        range_str = measurement_range if isinstance(measurement_range, str) else f"{measurement_range:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:VOLTAGE:DC? {range_str},{resolution}")).data)
    
    def measure_capacitance(self, measurement_range: Union[str|int] = 'AUTO', resolution: str = 'DEF') -> float:
        """Measures capacitance using a specified measurement range, on the 'PRIMARY' channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Farads), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured capacitance value.
        """
        try:
            assert isinstance(measurement_range, (float,int)) or measurement_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")
        
        try:
            assert resolution.upper() in {'DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'.")
        
        range_str = measurement_range if isinstance(measurement_range, str) else f"{measurement_range:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:CAPACITANCE? {range_str},{resolution}")).data)
    
    def measure_continuity_raw(self) -> float:
        """Performs a 2-wire continuity test.

        Returns:
            float: A resistance reading, as returned by the instrument during continuity tests. 
        """
        #TODO confirm return value when instrument sees an open circuit (>1.2 kOhm). Programmer guide is unclear.
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:CONTINUITY?")).data)
    
    def measure_continuity(self) -> bool:
        """Performs a 2-wire continuity test. The Keysight's internal threshold for continuity is 10 Ohms.

        Returns:
            bool: True if continuity is detected, otherwise false.
        """
        return True if self.measure_continuity_raw() <= 10.0 else False
    
    def measure_current_ac(self, measurement_range: Union[str|int|float] = 'AUTO', resolution: str = 'DEF') -> float:
        """Measures AC current using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured current value.
        """
        try:
            assert isinstance(measurement_range, (float,int)) or measurement_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")
        
        try:
            assert resolution.upper() in {'DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'.")
        
        range_str = measurement_range if isinstance(measurement_range, str) else f"{measurement_range:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:CURRENT:AC? {range_str},{resolution}")).data)
    
    def measure_current_dc(self, measurement_range: Union[str|int|float] = 'AUTO', resolution: str = 'DEF') -> float:
        """Measures DC current using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured current value.
        """
        try:
            assert isinstance(measurement_range, (float,int)) or measurement_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")
        
        try:
            assert resolution.upper() in {'DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'.")
        
        range_str = measurement_range if isinstance(measurement_range, str) else f"{measurement_range:.2e}"
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:CURRENT:DC? {range_str},{resolution}")).data)
    
    def measure_diode(self) -> float:
        """Performs a diode test.

        Returns:
            float: A voltage reading, as returned by the instrument during diode tests, if the voltage is in the range [0,1.2]. If the signal is greater than 1.2V then the value +9.9e+37 is returned. 
        """
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:DIODE?")).data)
    
    def measure_frequency(self, freq_range: Union[str|int|float] = 'DEF', freq_resolution: str = 'DEF', volt_range: Union[str|int|float] = 0.1) -> float:
        """Measures frequency of an AC volage signal at a desired resolution using a specified frequency range, on a specified channel.

        Before frequency measurement, the AC voltage range is configured. As per the programmer guide, the voltage range should be "at least" 0.1V for accurate frequency measurements.

        Args:
            freq_range (Union[str | int | float], optional): Specify a numeric value (in Hz), or one of {DEF|MAX|MIN}. MIN = DEF = 1 Hz, MAX = 1 MHz. Defaults to 'DEF'.
            freq_resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (freq_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            volt_range (Union[str | int | float], optional): Specify a numeric value (in V), or one of {AUTO|DEF|MAX|MIN}. Defaults to 0.1 V.

        Returns:
            float: The measured current value.
        """
        try:
            assert isinstance(freq_range, (float,int)) or freq_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for freq_range. Freq_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")
        
        try:
            assert freq_resolution.upper() in {'DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for freq_resolution. Resolution must be one of 'DEF','MAX','MIN'.")
        
        try:
            assert isinstance(volt_range, (float,int)) or volt_range.upper() in {'AUTO','DEF','MAX','MIN'} 
        except AssertionError:
            raise ValueError(f"Invalid value for volt_range. Volt_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'.")

        range_str = freq_range if isinstance(freq_range, str) else f"{freq_range:.2e}"
        self.transmission.command(f"SENSE:PRIMARY:FREQUENCY:VOLTAGE:RANGE {volt_range}")
        return float(self.transmission.poll(ASCII(f"MEASURE:PRIMARY:FREQUENCY? {range_str},{freq_resolution}")).data)
    
    def read_errors(self):
        i = 0
        while True:
            err = self.transmission.poll(ASCII(f"SYST:ERR?")).data
            print(err)
            i += 1
            if err == '+0, "No error"' or i >= 20:
                break


