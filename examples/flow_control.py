from epcomms.equipment.flowcontroller import AlicatEIP

controller = AlicatEIP("192.168.0.172")

print(controller.get_setpoint())
print(controller.get_identity_string())
controller.set_setpoint(1.0)
print(controller.get_setpoint())
controller.set_setpoint(0.0)
print(controller.get_setpoint())
print(controller._get_device_readings())

controller.reset_totalizer()

