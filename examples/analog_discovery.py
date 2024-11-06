from epcomms.equipment.analog_discovery import AnalogDiscovery

from epcomms.equipment.function_generator import FunctionGeneratorMode

import time
from ctypes import c_int, c_double


devices = AnalogDiscovery.list_devices()

print(devices)

device = AnalogDiscovery('192.168.0.32', '210018B9D801')

device.function_generator.set_mode(FunctionGeneratorMode.SINE, 0)
device.function_generator.set_frequency(0.05, 0)
device.function_generator.set_amplitude(1, 0)
device.function_generator.set_offset(1,0)
#device.function_generator.set_duty_cycle(50, 0)
device.function_generator.start_output(0, False)
time.sleep(30)
device.function_generator.disable_output(0)




