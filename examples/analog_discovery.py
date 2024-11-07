from epcomms.equipment.analog_discovery import AnalogDiscovery

from epcomms.equipment.function_generator import FunctionGeneratorMode

import time
from ctypes import c_int, c_double


devices = AnalogDiscovery.list_devices()

print(devices)

device = AnalogDiscovery('192.168.0.32', '210018B9D801')

# device.function_generator.set_mode(FunctionGeneratorMode.SINE, 0)
# device.function_generator.set_frequency(0.05, 0)
# device.function_generator.set_amplitude(1, 0)
# device.function_generator.set_offset(1,0)
# device.function_generator.start_output(0, False)
# time.sleep(30)
# device.function_generator.disable_output(0)

voltage = 0

device.daq.configure_daq_channel(0, 5, 0)


for i in range(5):
    voltage += device.daq.measure_voltage(0)

voltage = voltage/5
print(voltage)

device.daq.configure_daq_channel(0, 5, -1*voltage)

voltage = device.daq.measure_voltage(0)

print(voltage)






