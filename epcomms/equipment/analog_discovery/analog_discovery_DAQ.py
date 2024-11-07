from ctypes import *
from . import dwfconstants
import socket
import time


from epcomms.connection.transmission.transmission import Transmission
from epcomms.equipment.daq import DAQ

from . import dwf
from .dwfconstants import *


class AnalogDiscoveryDAQ(DAQ):
    def __init__(self, device_handle: c_int) -> None:
        self.transmission = None # We don't directly send packets to this device
        self.handle = device_handle

    def measure_voltage(self, channel: int) -> float:
        """Perform a single, untriggered voltage measurement."""
        num_samples = 100
        rgdSamples = (c_double*num_samples)()

        dwf.FDwfAnalogInFrequencySet(self.handle, c_double(20000000.0))
        dwf.FDwfAnalogInBufferSizeSet(self.handle, c_int(num_samples)) 
        dwf.FDwfAnalogInChannelEnableSet(self.handle, c_int(channel), c_int(1))
        dwf.FDwfAnalogInChannelFilterSet(self.handle, c_int(channel), c_int(1))


        dwf.FDwfAnalogInConfigure(self.handle, c_int(channel), c_int(1))

        sts = c_byte()
        while True:
            dwf.FDwfAnalogInStatus(self.handle, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value :
                break
            time.sleep(0.1)
            print("sleeping")

        dwf.FDwfAnalogInStatusData(self.handle, c_int(channel), rgdSamples, c_int(num_samples)) # get channel 1 data

        return sum(rgdSamples)/len(rgdSamples)



    def configure_daq_channel(self, channel: int, voltage_range: float, offset_voltage: float) -> None:
        """Configures a channel of an instrument as a DAQ."""
        dwf.FDwfAnalogInChannelRangeSet(self.handle, c_int(channel), c_double(voltage_range))
        dwf.FDwfAnalogInChannelOffsetSet(self.handle, c_int(channel), c_double(offset_voltage))
