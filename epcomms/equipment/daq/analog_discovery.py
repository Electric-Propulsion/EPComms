"""
Analog Discovery Device Control
This module provides an interface to control an analog discovery multi-function device.
"""

from WF_SDK import device, scope, dmm, wavegen, supplies   # import instruments

from . import DAQ

class Analog_Discovery(DAQ):

    def __init__(self, device_name: str | None = None) -> None:
        """Generate an Analog Discovery device.

        Args:
            device_name (str): One of the following optons:
                None (first device), 
                "Analog Discovery", 
                "Analog Discovery 2", 
                "Analog Discovery Studio", 
                "Digital Discovery", 
                "Analog Discovery Pro 3X50", 
                "Analog Discovery Pro 5250"
        """

        self.name: str = device_name

        # Note that this is a reference to a global variable (sigh)
        self.device_data: device.data | None = None

    ####################
    # Device
    ####################

    def device_open(self) -> None:
        # config=0 means automatic config
        self.device_data = device.open(device=self.name, config=0)

    def device_close(self) -> None:
        device.close(self.device_data)

    def device_get_info(self) -> device.data:
        return self.device_data

    ####################
    # Oscilloscope
    ####################

    def scope_open(self, sampling_frequency: float = 20E6, buffer_size: int = 0, offset: int = 0, amplitude_range: int = 5) -> None:
        """Configures and opens the oscilloscope.

        Args:
            sampling_frequency (float, optional): Defaults to 20E6.
            buffer_size (int, optional): Set to 0 for maximum. Defaults to 0.
            offset (int, optional): Offset voltage in Volts. Defaults to 0.
            amplitude_range (int, optional): Amplitude range in Volts. Defaults to 5.
        """
        scope.open(self.device_data, sampling_frequency, buffer_size, offset, amplitude_range)

    def scope_close(self) -> None:
        scope.close(self.device_data)
    
    def scope_measure(self, channel: int) -> float:
        """Take one voltage measurement.

        Args:
            channel (int): Choose channel 1-4

        Returns:
            float: Measured value.
        """
        return scope.measure(self.device_data, channel)
        
    
    def scope_record(self, channel: int) -> list[float]:
        # TODO: continue implementing from here.
        return
    
    def scope_trigger(self, channel: int, source: str, enable: bool, level: float, edge_rising: bool = True) -> list[float]:
        return
    
    ####################
    # Signal Generator
    ####################

    
    def wavegen_open(self) -> None:
        return

    def wavegen_close(self) -> None:
        return
    
    def wavegen_generate(self, channel: int, function: str, offset: float, frequency: float, amplitude: float, symmetry: float, wait_time: float, run_time: float, repeat_count: float, input_data: list[float]) -> None:
        return
    
    def wavegen_enable_channel(self, channel: int) -> None:
        return
    
    def wavegen_disable_channel(self, channel: int) -> None:
        return
    
    ####################
    # Power Supply
    ####################

    def psu_open(self) -> None:
        return

    def psu_close(self) -> None:
        return
    
    def psu_switch(self) -> None:
        # Todo define params if needed
        return
    
    ####################
    # Multimeter
    ####################

    def dmm_open(self) -> None:
        return
    
    def dmm_close(self) -> None:
        return
    
    def dmm_measure(self, mode: str, range: float, high_impedance: bool) -> None:
        return