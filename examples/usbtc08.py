from epcomms.equipment.temperature_sensor import PicoUSBTC08
import time

def test1():
    pico = PicoUSBTC08('192.168.0.192', 8001)

    pico.open_instrument()

    for i in range(0,8):
        pico.configure_channel(i+1, 'K')

    result = pico.measure_all_channels()
    print(result)

    pico.disable_channel(8)
    result = pico.measure_all_channels()

    pico.close_instrument()
    

if __name__ == "__main__":
    tests = [
        test1,
    ]

    for t in tests:
        t()
        # try:
        #     t()
        # except:
        #     print("Fail")