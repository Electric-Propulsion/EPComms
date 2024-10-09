from ctypes import *
from . import dwfconstants
import socket


from epcomms.connection.transmission.transmission import Transmission
from epcomms.equipment.function_generator import FunctionGenerator, FunctionGeneratorMode
from epcomms.equipment.daq import DAQ

from . import dwf

class AnalogDiscovery(FunctionGenerator, DAQ):



    @classmethod
    def list_devices(cls) -> dict[int, str]:
        num_devices = c_int(0)
        devices: dict[str, int] = {} #index, serial number

        dwf.FDwfEnum(dwfconstants.enumfilterAll, byref(num_devices))
        for device_index in range(0, num_devices.value):
            device_sn = create_string_buffer(16)
            dwf.FDwfEnumSN (c_int(device_index), device_sn)
            serial_number_string = str(device_sn.value.decode('utf-8')).split(":")[-1]
            devices[serial_number_string] = device_index
        return devices
    
    @classmethod
    def wake_networked_device(cls, ip_addr: str):
        # I haven't really been able to test this, not sure if it works
        timeout_s = 5
        try:
            socket.setdefaulttimeout(timeout_s)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_addr, 17))
        except OSError as error:
            return False
        else:
            s.close()
            return True


    def __init__(self, ip_addr: str, serial_number: str):
        transmission = None # We don't directly send packets to this device
        FunctionGenerator.__init__(self, transmission)
        DAQ.__init__(self, transmission)

        devices = self.list_devices()
        if serial_number not in devices:
            # It might need to be woken
            # This hasn't been tested
            self.wake_networked_device(ip_addr)
            devices = self.list_devices()
            if serial_number not in devices:
                # The device ain't here, raise an exception
                raise ValueError("The specified serial number was not found")
            
        self.device_handle = c_int()

        device_index = devices[serial_number]

        dwf.FDwfDeviceOpen(c_int(device_index), byref(self.device_handle))

        if self.device_handle.value == dwfconstants.hdwfNone.value:
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            raise ConnectionError(f"Failed to open Analog Discovery device: {szerr.value}")




    def configure_daq_channel(self, channel: int, voltage_range: float, offset_voltage: float) -> None:
        return super().configure_daq_channel(channel, voltage_range, offset_voltage)
    
    @property
    def channels(self):
        return super().channels

    def disable_output(self, channel: int) -> None:
        return super().disable_output(channel)
    
    def get_amplitude(self, channel: int) -> float:
        return super().get_amplitude(channel)
    
    def get_duty_cycle(self, channel: int) -> float:
        return super().get_duty_cycle(channel)
    
    def get_frequency(self, channel: int) -> float:
        return super().get_frequency(channel)
    
    def get_mode(self, channel: int) -> FunctionGeneratorMode:
        return super().get_mode(channel)
    
    def get_offset(self, channel: int) -> float:
        return super().get_offset(channel)
    
    def get_phase(self, channel: int) -> float:
        return super().get_phase(channel)
    
    def measure_voltage(self, channel: int) -> float:
        return super().measure_voltage(channel)
    
    def set_amplitude(self, amplitude: float, channel: int) -> None:
        return super().set_amplitude(amplitude, channel)
    
    def set_duty_cycle(self, duty_cycle: float, channel: int) -> None:
        return super().set_duty_cycle(duty_cycle, channel)
    
    def set_frequency(self, frequency: float, channel: int) -> None:
        return super().set_frequency(frequency, channel)
    
    def set_mode(self, mode: FunctionGeneratorMode, channel: int) -> None:
        return super().set_mode(mode, channel)
    
    def set_offset(self, offset: float, channel: int) -> None:
        return super().set_offset(offset, channel)
    def set_phase(self, phase: float, channel: int) -> None:
        return super().set_phase(phase, channel)
    
    def start_output(self, channel: int, repeat: bool) -> None:
        return super().start_output(channel, repeat)



        


