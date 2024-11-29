from epcomms.equipment.vacuumcontroller import Terranova962A

controller = Terranova962A('/dev/ttyUSB0')

print(controller.get_gauge_type())
print(controller.get_identity())
try:
    print(controller.get_pressure_gauge_1())
except:
    pass
print(controller.get_units())
try:
    print(controller.get_pressure_gauge_2())
except:
    pass