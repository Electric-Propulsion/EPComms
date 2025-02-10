from epcomms.equipment.powersupply import BK1694
import time

def test():
    psu = BK1694("192.168.0.156")

    psu.set_voltage(27)
    time.sleep(10)
    psu.set_output(True)
    time.sleep(10)
    voltage = psu.measure_voltage_setpoint()
    print(f"Voltage setpoint: {voltage}V")
    time.sleep(15)
    psu.set_output(False)

    psu.close()

if __name__ == "__main__":
    test()