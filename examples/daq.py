import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators
 
# load the dynamic library, get constants path (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = ctypes.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"
 
# import constants
path.append(constants_path)
import dwfconstants as constants

class Data:
    """ stores the sampling frequency and the buffer size """
    handle = ctypes.c_int(0)
    sampling_frequency = 20e06
    buffer_size = 8192
 
def open(device_data, sampling_frequency=20e06, buffer_size=8192, offset=0, amplitude_range=5):
    """
        initialize the oscilloscope
        parameters: - device data
                    - sampling frequency in Hz, default is 20MHz
                    - buffer size, default is 8192
                    - offset voltage in Volts, default is 0V
                    - amplitude range in Volts, default is ±5V
    """
    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int()
    # connect to the first available device
    dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(device_handle))
    data.handle = device_handle

    # enable all channels
    dwf.FDwfAnalogInChannelEnableSet(device_data.handle, ctypes.c_int(0), ctypes.c_bool(True))
 
    # set offset voltage (in Volts)
    dwf.FDwfAnalogInChannelOffsetSet(device_data.handle, ctypes.c_int(0), ctypes.c_double(offset))
 
    # set range (maximum signal amplitude in Volts)
    dwf.FDwfAnalogInChannelRangeSet(device_data.handle, ctypes.c_int(0), ctypes.c_double(amplitude_range))
 
    # set the buffer size (data point in a recording)
    dwf.FDwfAnalogInBufferSizeSet(device_data.handle, ctypes.c_int(buffer_size))
 
    # set the acquisition frequency (in Hz)
    dwf.FDwfAnalogInFrequencySet(device_data.handle, ctypes.c_double(sampling_frequency))
 
    # disable averaging (for more info check the documentation)
    dwf.FDwfAnalogInChannelFilterSet(device_data.handle, ctypes.c_int(-1), constants.filterDecimate)
    data.sampling_frequency = sampling_frequency
    data.buffer_size = buffer_size
    return

def measure_voltage(device_data, channel):
    """
        measure a voltage
        parameters: - device data
                    - the selected oscilloscope channel (1-2, or 1-4)
 
        returns:    - the measured voltage in Volts
    """
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_data.handle, ctypes.c_bool(False), ctypes.c_bool(False))
 
    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(device_data.handle, ctypes.c_bool(False), ctypes.c_int(0))
 
    # extract data from that buffer
    voltage = ctypes.c_double()   # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(device_data.handle, ctypes.c_int(channel - 1), ctypes.byref(voltage))
 
    # store the result as float
    voltage = voltage.value
    return voltage  

def _switch_digital_(device_data, master_state, voltage):
    """
        turn the power supplies on/off
        parameters: - device data
                    - master switch - True = on, False = off
                    - supply voltage in Volts
    """
    # set supply voltage
    voltage = max(1.2, min(3.3, voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(voltage))
 
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(master_state))
    return

def close(device_data):
    """
        close a specific device
    """
    dwf.FDwfDeviceClose(device_data.handle)
    return

data = Data()
open(data)
msmts = []
# _switch_digital_(data, True, 1.5)
msmts.append(measure_voltage(data, 1))
msmts.append(measure_voltage(data, 2))
msmts.append(measure_voltage(data, 3))
msmts.append(measure_voltage(data, 4))
# _switch_digital_(data, False, 1.5)
print(data.handle)
print(msmts)

close(data)