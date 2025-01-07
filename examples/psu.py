from epcomms.equipment.powersupply import KeysightEDU36311A
import time

def test1():

    # psu = KeysightEDU36311A("TCPIP::K-EDU36311A::inst0::INSTR")
    psu = KeysightEDU36311A("TCPIP::192.168.0.145::INSTR")

    psu.beep()

    for channel in range(1,4):
        psu.disable_output(channel)

    for channel in range(1,4):
        psu.set_current(0.050, channel)

    psu.set_voltage(27, 2)
    psu.set_voltage(29,3)
    psu.set_voltage(1,1)


    time.sleep(1)

    for channel in range(1,4):
        psu.enable_output(channel)
        time.sleep(1)

    for channel in range(1,4):
        voltage = psu.measure_voltage(channel)
        current = psu.measure_current(channel)
        print(f"Channel {channel}: {voltage}V {current}A")

    time.sleep(1)

    for channel in range(1,4):
        psu.disable_output(channel)

    psu.beep()

    psu.close()

def test2_reconnect():
    for i in range(5):
        psu = KeysightEDU36311A("TCPIP::192.168.0.145::INSTR")
        psu.beep()
        voltage = psu.measure_voltage(1)
        print(f"Channel 1: {voltage}V")
        psu.close()

if __name__ == "__main__":
    tests = [
        # test1,
        test2_reconnect,
    ]

    for t in tests:
        t()
        # try:
        #     t()
        # except:
        #     print("Fail")