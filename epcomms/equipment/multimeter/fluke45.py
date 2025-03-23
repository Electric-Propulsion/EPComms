# pylint: disable=missing-module-docstring
# TODO: Add docstrings # pylint: disable=fixme
from . import Multimeter
from epcomms.connection.transmission import Serial
from epcomms.connection.packet import ASCII
from typing import Union
import time


class Fluke45(Multimeter):
    # pylint: disable=missing-class-docstring
    # pylint: disable=too-few-public-methods
    def __init__(self, device_location, meas_rate: Union["F", "M", "S"] = "F"):
        if meas_rate not in ["F", "M", "S"]:
            raise ValueError("Invalid measurement rate")
        self.transmission = Serial(device_location, terminator="\r")

        # set up the multimeter to take measurements at the specified rate
        self.transmission.poll(ASCII(f"RATE {meas_rate}\r"))
        self.transmission.poll(ASCII("TRIGGER 1\r"))
        self.transmission.poll(ASCII("AUTO\r"))
    def measure_voltage_ac(self, measurement_range, resolution) -> float:
        # pylint: disable=unused-argument
        raise NotImplementedError
    
    def measure_voltage_dc(self, measurement_range = None, resolution = None) -> float:
        # pylint: disable=unused-argument
        self.transmission.poll(ASCII("VDC\r"))
        time.sleep(0.1)
        data = self.transmission.poll(ASCII("VAL1?\r")).data
        time.sleep(0.1)
        self.transmission.read()
        return float(data)

    
    def measure_capacitance(self, measurement_range, resolution) -> float:
        # pylint: disable=unused-argument
        raise NotImplementedError
    
    def measure_continuity(self) -> bool:
        raise NotImplementedError
    
    def measure_current_ac(self, measurement_range, resolution) -> float:
        # pylint: disable=unused-argument
        raise NotImplementedError
    
    def measure_current_dc(self, measurement_range, resolution) -> float:
        # cause this is quick and dirty, ignoring the arguments
        self.transmission.command(ASCII("ADC"))
        data = self.transmission.poll(ASCII("VAL1?")).data
        return float(data)
    
    def measure_frequency(self, freq_range, freq_resolution, volt_range) -> float:
        # pylint: disable=unused-argument
        raise NotImplementedError

