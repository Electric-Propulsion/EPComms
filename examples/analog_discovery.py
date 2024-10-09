from epcomms.equipment.analog_discovery import AnalogDiscovery



devices = AnalogDiscovery.list_devices()

print(devices)

device = AnalogDiscovery('192.168.0.32', '210018B9D801')
