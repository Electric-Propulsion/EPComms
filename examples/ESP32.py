from epcomms.equipment.powersupply import BK1694

def test():
    psu = BK1694("192.168.0.156")

    psu.set_voltage(27)
    psu.set_output(True)

    voltage = psu.measure_voltage_setpoint()

    print(f"Voltage setpoint: {voltage}V")

    psu.set_output(False)

    psu.close()

if __name__ == "__main__":
    test()