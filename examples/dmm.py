import time

from epcomms.equipment.multimeter.keysight_edu34450a import KeysightEDU34450A


def test1():
    # dmm = KeysightEDU34450A("TCPIP::K-34450A-50039::inst0")
    dmm = KeysightEDU34450A("USB0::10893::36353::CN62350039::0::INSTR")

    dmm.beep()

    meas = dmm.measure_voltage_dc()
    print("DC Voltage (primary channel; autoranging): " + str(meas))

    meas = dmm.measure_voltage_dc(measurement_range=100)
    print("DC Voltage (primary channel; range of 100V): " + str(meas))

    meas = dmm.measure_voltage_dc(measurement_range=100, resolution="MIN")
    print(
        "DC Voltage (primary channel; range of 100V and MIN resolution): " + str(meas)
    )

    meas = dmm.measure_capacitance()
    print("Capacitance (autoranging): " + str(meas))

    meas = dmm.measure_continuity()
    print("Continuity [Resistance]: " + str(meas))

    meas = dmm.measure_diode()
    print("Diode [Voltage]: " + str(meas))

    # dmm.read_errors()

    time.sleep(1)
    dmm.beep()

    dmm.close()


def test2_reconnect():
    for _ in range(5):
        dmm = KeysightEDU34450A("TCPIP::192.168.0.121::INSTR")
        dmm.beep()
        meas = dmm.measure_voltage_dc(measurement_range=100, resolution="MIN")
        print(
            "DC Voltage (primary channel; range of 100V and MIN resolution): "
            + str(meas)
        )
        dmm.close()


if __name__ == "__main__":
    tests = [
        test1,
        # test2_reconnect,
    ]

    for t in tests:
        t()
        # try:
        #     t()
        # except:
        #     print("Fail")
