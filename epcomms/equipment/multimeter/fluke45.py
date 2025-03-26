# pylint: disable=missing-module-docstring
# TODO: Add docstrings # pylint: disable=fixme
from . import Multimeter
from epcomms.connection.transmission import Serial, TransmissionError
from epcomms.connection.packet import ASCII
from typing import Union
import time


class Fluke45(Multimeter):
    # pylint: disable=missing-class-docstring
    # pylint: disable=too-few-public-methods
    def __init__(self, device_location: str, default_meas_rate: str = "F") -> None:
        if default_meas_rate not in ["F", "M", "S"]:
            raise ValueError("Invalid default measurement rate")
        self.transmission = Serial(device_location, terminator="\r")

        # set up the multimeter to take measurements at the specified rate
        self.transmission.poll(ASCII(f"RATE {default_meas_rate}\r"))
        self.transmission.poll(ASCII("TRIGGER 1\r"))
        self.transmission.poll(ASCII("AUTO\r"))

    def read_fluke_status(self) -> None:
        # Just read the status string it sends back every time it takes a measurement and raise an error 
        # if it's unhappy

        status = self.transmission.read().data
        if len(status) != 2 or status[1] != ">":
            raise TransmissionError("Fluke 45 Invalid status string")
        if status[0] == "?":
            raise TransmissionError("Fluke 45 Command Error")
        if status[0] == "!":
            raise TransmissionError("Fluke 45 Execution Error")

    def set_range(self, measurement_range: Union[float, "AUTO", None]) -> None:
        if measurement_range is None:
            return # Use whatever range has been configured 
        if measurement_range == "AUTO":
            self.transmission.command(ASCII("AUTO\r"))
            self.read_fluke_status()
            return
        if 1<= measurement_range <= 7:
            self.transmission.command(ASCII(f"RANGE {measurement_range}\r"))
            self.read_fluke_status()
            return
        
        raise ValueError("Invalid Measurement range for Fluke 45. Must be AUTO or between 1 and 7")
    
    def set_resolution(self, resolution: Union["S","M","F", None]) -> None: # Actually rate
        # Resolution is "rate"
        if resolution is None:
            return # Use whatever resolution has been configured
        if resolution in ["S","M","F"]:
            self.transmission.command(ASCII(f"RATE {resolution}\r"))
            self.read_fluke_status()
            return
        raise ValueError("Invalid resolution for Fluke 45. Must be S, M, or F")

    def measure_voltage_ac(self, measurement_range = None, resolution = None) -> float:
        self.set_range(measurement_range)
        self.set_resolution(resolution)
        self.transmission.command(ASCII("VAC\r")) # set the multimeter to measure AC voltage
        self.read_fluke_status() # read the status string to make sure the multimeter is happy

        data = self.transmission.poll(ASCII("VAL1?\r")).data # poll the multimeter for the measurement
        self.read_fluke_status() # read the status string to make sure the multimeter is happy
        return float(data) # return the measurement
    
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
        raise NotImplementedError("The Fluke 45 does not support capacitance measurements")
    
    def measure_continuity_raw(self) -> bool:
        self.transmission.command(ASCII("CONT\r"))
        self.read_fluke_status()
        self.transmission.poll(ASCII("VAL1?\r"))
        self.read_fluke_status()
        return float(self.transmission.read().data)
    
    def measure_continuity(self) -> bool:
        return self.measure_continuity_raw() < 0.025
    
    def measure_current_ac(self, measurement_range = None, resolution = None) -> float:
        # pylint: disable=unused-argument
        self.transmission.command(ASCII("AAC"))
        self.read_fluke_status()
        self.set_range(measurement_range)
        self.set_resolution(resolution)
        data = self.transmission.poll(ASCII("VAL1?\r")).data
        self.read_fluke_status()
        return float(data)


    def measure_current_dc(self, measurement_range = None, resolution = None) -> float:
        # cause this is quick and dirty, ignoring the arguments
        self.transmission.command(ASCII("ADC"))
        self.read_fluke_status()
        self.set_range(measurement_range)
        self.set_resolution(resolution)
        data = self.transmission.poll(ASCII("VAL1?")).data
        self.read_fluke_status()
        return float(data)
    
    def measure_frequency(self, freq_range = None, freq_resolution = None, volt_range = None) -> float:
        if volt_range is not None:
            raise ValueError("The Fluke 45 does not support setting the voltage range for frequency measurements")
        self.transmission.command(ASCII("FREQ"))
        self.read_fluke_status()
        self.set_range(freq_range)
        self.set_resolution(freq_resolution)
        data = self.transmission.poll(ASCII("VAL1?")).data
        self.read_fluke_status()
        return float(data)

        

