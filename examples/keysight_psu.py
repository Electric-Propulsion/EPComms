from epcomms.equipment.powersupply import KeysightEDU36311A
import time

from epcomms.connection.transmission.visa import Visa

print(Visa.list_resources())

psu = KeysightEDU36311A("TCPIP0::192.168.0.145::inst0::INSTR")
try:
    psu.beep()

    for channel in range(1, 4):
        psu.set_output(False, channel)

        time.sleep(1)
        print(psu.get_output(channel))
        assert psu.get_output(channel) is False

        i_tgt = 0.050
        psu.set_current_limit(i_tgt, channel)
        time.sleep(0.5)
        i_setpoint = psu.measure_current_limit(channel)

        assert abs(i_tgt - i_setpoint) < 0.001

        v_tgt = 5
        psu.set_voltage(5, channel)
        time.sleep(0.5)
        v_setpoint = psu.measure_voltage_setpoint(channel)

        assert abs(v_tgt - v_setpoint) < 0.001

        psu.set_output(True, channel)

        time.sleep(1)

        assert psu.get_output(channel) is True

        v = psu.measure_voltage(channel)
        i = psu.measure_current(channel)

        print(f"Channel {channel}: {v}V {i}A (set to {v_tgt}V {i_tgt}A)")
        assert abs(v - v_tgt) < 0.1

        time.sleep(1)
finally:
    psu.close()