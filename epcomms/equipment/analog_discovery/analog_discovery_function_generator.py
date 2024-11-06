from ctypes import *
from . import dwfconstants
import socket


from epcomms.connection.transmission.transmission import Transmission
from epcomms.equipment.function_generator import (
    FunctionGenerator,
    FunctionGeneratorMode,
)
from epcomms.equipment.daq import DAQ

from . import dwf

class AnalogDiscoveryFunctionGenerator(FunctionGenerator):
    def __init__(self, device_handle: c_int) -> None:
        self.transmission = None # We don't directly send packets to this device
        self.handle = device_handle
        self._channels = self.channels
        self.node = c_int(0) # Hardcoded to be he carrier node (no AM or FM modulation)\
        dwf.FDwfDeviceAutoConfigureSet(self.handle, c_int(0)) 


    def set_mode(self, mode: FunctionGeneratorMode, channel: int) -> None:
        """Sets the mode of the function generator."""
        dwf.FDwfAnalogOutNodeFunctionSet(self.handle, self.node, c_int(channel), c_int(1))
    
    def get_mode(self, channel: int) -> FunctionGeneratorMode:
        """Gets the mode of the function generator."""
        mode = c_int()
        dwf.FDwfAnalogOutNodeFunctionGet(self.handle, self.node, c_int(channel), byref(c_int(mode)))
        return FunctionGeneratorMode(mode.value)
    
    def set_frequency(self, frequency: float, channel: int) -> None:
        """Sets the frequency of the function generator."""
        dwf.FDwfAnalogOutNodeFrequencySet(self.handle, self.node, c_int(channel), c_double(frequency))

    def get_frequency(self, channel: int) -> float:
        """Gets the frequency of the function generator."""
        frequency = c_double()
        dwf.FDwfAnalogOutNodeFrequencyGet(self.handle, self.node, c_int(channel), byref(frequency))
        return frequency.value
    
    def set_amplitude(self, amplitude: float, channel: int) -> None:
        """Sets the amplitude of the function generator."""
        dwf.FDwfAnalogOutNodeAmplitudeSet(self.handle, self.node, c_int(channel), c_double(amplitude))

    def get_amplitude(self, channel: int) -> float:
        """Gets the amplitude of the function generator."""
        amplitude = c_double()
        dwf.FDwfAnalogOutNodeAmplitudeGet(self.handle, self.node, c_int(channel), byref(amplitude))
        return amplitude.value
        
    def set_offset(self, offset: float, channel: int) -> None:
        """Sets the offset of the function generator."""
        dwf.FDwfAnalogOutNodeOffsetSet(self.handle, self.node, c_int(channel), c_double(offset))

    def get_offset(self, channel: int) -> float:
        """Gets the offset of the function generator."""
        offset = c_double()
        dwf.FDwfAnalogOutNodeOffsetGet(self.handle, self.node, c_int(channel), byref(offset))
        return offset.value

    def set_duty_cycle(self, duty_cycle: float, channel: int) -> None:
        """Sets the duty cycle of the function generator."""
        dwf.FDwfAnalogOutNodeSymmetrySet(self.handle, self.node, c_int(channel), c_double(duty_cycle))  

    def get_duty_cycle(self, channel: int) -> float:
        """Gets the duty cycle of the function generator."""
        duty_cycle = c_double()
        dwf.FDwfAnalogOutNodeSymmetryGet(self.handle, self.node, c_int(channel), byref(duty_cycle))
        return duty_cycle.value
        
    def set_phase(self, phase: float, channel: int) -> None:
        """Sets the phase of the function generator."""
        dwf.FDwfAnalogOutNodePhaseSet(self.handle, self.node, c_int(channel), c_double(phase))
        
    def get_phase(self, channel: int) -> float:
        """Gets the phase of the function generator."""
        phase = c_double()
        dwf.FDwfAnalogOutNodePhaseGet(self.handle, self.node, c_int(channel), byref(phase))
        return phase.value

    def start_output(self, channel: int, repeat: bool) -> None:
        """Enables the output of the function generator."""
        dwf.FDwfAnalogOutRepeatSet(self.handle, c_int(channel), c_int(repeat))
        dwf.FDwfAnalogOutNodeEnableSet(self.handle, channel, self.node, c_int(1))
        dwf.FDwfAnalogOutConfigure(self.handle, c_int(channel), 1) # 1 = start output

    def disable_output(self, channel: int) -> None:
        """Disables the output of the function generator."""
        dwf.FDwfAnalogOutNodeOffsetSet(self.handle, self.node, c_int(channel), c_double(0))
        dwf.FDwfAnalogOutNodeEnableSet(self.handle, channel, self.node, c_int(0))
        dwf.FDwfAnalogOutConfigure(self.handle, c_int(channel), 0) # 0 = stop output
    
    @property
    def channels(self) -> int:
        """Returns the number of channels on the function generator."""
        channels = c_int()
        dwf.FDwfAnalogOutCount(self.handle, byref(channels))
        return channels.value

