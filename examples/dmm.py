from epcomms.equipment.multimeter.keysight_edu34450a import KeysightEDU34450A
import time

dmm = KeysightEDU34450A("TCPIP::K-EDU34450A::inst0::INSTR")
#TODO: understand what the transmission is supposed to be and insert the correct string

dmm.beep()

meas = dmm.measure_voltage_dc()
print("DC Voltage (autoranging): " + str(meas))

meas = dmm.measure_voltage_dc(channel='SECONDARY')
print("DC Voltage (secondary channel): " + str(meas))

meas = dmm.measure_voltage_dc(range=100, resolution=3E-5)
print("AC Voltage (primary channel; range of 100V and resolution of 3E-5 V): " + str(meas))

meas = dmm.measure_capacitance()
print("Capacitance (autoranging): " + str(meas))

meas = dmm.measure_continuity()
print("Continuity [Resistance]: " + str(meas))

meas = dmm.measure_diode()
print("Diode [Voltage]: " + str(meas))

meas = dmm.measure_resistance()
print("Resistance: " + str(meas))

time.sleep(1)
dmm.beep()