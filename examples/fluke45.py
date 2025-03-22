from epcomms.equipment.multimeter.fluke45 import Fluke45

mm = Fluke45("COM4")
for i in range(10):
    print(mm.measure_voltage_dc(None,None))
