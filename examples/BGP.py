from epcomms.equipment.vacuumcontroller.inficon_BGP400 import InficonBGP400
import time
import logging

logging.basicConfig(level=logging.DEBUG)    
def main():
    bgp400 = InficonBGP400("COM3")
    bgp400.set_mbar()
    #bgp400.degass_on()
    time.sleep(2)
    print(bgp400.get_state().pressure)
    while True:
        try:
            print(bgp400.get_state().pressure)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    