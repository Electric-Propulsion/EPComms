from ctypes import *
from . import dwfconstants
import socket


from epcomms.connection.transmission.transmission import Transmission
from epcomms.equipment.daq import DAQ

from . import dwf

class AnalogDiscoveryDAQ(DAQ):
    def __init__(self, device_handle: c_int) -> None:
        self.transmission = None # We don't directly send packets to this device
        self.handle = device_handle

    def measure_voltage(self, channel: int) -> float:
        pass

    def configure_daq_channel(self, channel: int, voltage_range: float, offset_voltage: float) -> None:
        pass
