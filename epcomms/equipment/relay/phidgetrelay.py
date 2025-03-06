from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *

from . import Relay


class PhidgetRelay(Relay):

    def __init__(self, serial_number: int, channel: int) -> None:
        
        self.channel = DigitalOutput()
        self.channel.setDeviceSerialNumber(serial_number) # 9137
        self.channel.setChannel(channel) # 0
        self.channel.open()


    def close(self):
        self.channel.close()

    def set_state(self, state: Relay.State) -> None:
        match state:
            case Relay.State.OPEN:
                self.channel.setState(False)
            case Relay.State.CLOSED:
                self.channel.setState(True)
            case _:
                raise ValueError("Invalid state")

    