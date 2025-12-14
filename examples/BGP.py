from epcomms.equipment.vacuumcontroller.inficon_BGP400 import InficonBGP400

def main():
    bgp400 = InficonBGP400("COM3")
    bgp400.set_mbar()
    #bgp400.degass_on()
    print(bgp400.get_state().pressure)

if __name__ == "__main__":
    main()