from epcomms.equipment.multimeter import TektronixDMM4050
import time
dmm = TektronixDMM4050("192.168.0.136", 3490)

try:
    dmm.display_text("'sup bitches")
    time.sleep(1)
    dmm.clear_text()
    time.sleep(1)
    dmm.beep()
    time.sleep(1)

    dmm.measure_continuity()
    time.sleep(1)

    print(dmm.measure_voltage_dc())
    print(dmm.measure_voltage_ac())
    print(dmm.measure_current_dc())
    print(dmm.measure_current_ac())
    print(dmm.measure_capacitance())
    print(dmm.measure_frequency())
    time.sleep(1)

    for i in range(10):
        dmm.display_text(f"{10-i}")
        time.sleep(1)
        voltage = dmm.measure_voltage_dc()
        print(f"Voltage: {voltage}")
        dmm.display_text(f"{voltage:.2f}V")
        time.sleep(1)

finally:
    dmm.close()
