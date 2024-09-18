from epcomms.equipment.vacuumcontroller import Terranova962A

controller = Terranova962A('/dev/ttyUSB0')

print(controller.get_gauge_type())
print(controller.get_identity())
print(controller.get_pressure_gauge_1())
print(controller.get_units())
print(controller.get_pressure_gauge_2())