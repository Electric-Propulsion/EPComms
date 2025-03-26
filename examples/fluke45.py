from epcomms.equipment.multimeter.fluke45 import Fluke45
import time

mm = Fluke45("/dev/ttyUSB0")

print(mm.measure_continuity())
time.sleep(1)


for _range in [None, 'AUTO', 1, 2, 3, 4, 5, 6, 7]:
    for resolution in [None, 'S', 'M', 'F']:
        try:
            print(mm.measure_voltage_ac(_range, resolution))
        except Exception as e:
            print(f"Error measuring voltage AC with range {_range} and resolution {resolution}: {e}")
        time.sleep(1)

        try:
            print(mm.measure_voltage_dc(_range, resolution))
        except Exception as e:
            print(f"Error measuring voltage DC with range {_range} and resolution {resolution}: {e}")
        time.sleep(1)

        try:
            print(mm.measure_current_ac(_range, resolution))
        except Exception as e:
            print(f"Error measuring current AC with range {_range} and resolution {resolution}: {e}")
        time.sleep(1)

        try:
            print(mm.measure_current_dc(_range, resolution))
        except Exception as e:
            print(f"Error measuring current DC with range {_range} and resolution {resolution}: {e}")
        time.sleep(1)

        try:
            print(mm.measure_frequency(_range, resolution))
        except Exception as e:
            print(f"Error measuring frequency with range {_range} and resolution {resolution}: {e}")
        time.sleep(1)


print("DONE")


