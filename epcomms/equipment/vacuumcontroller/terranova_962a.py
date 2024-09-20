from typing import Union, Literal
from epcomms.connection.packet import ASCII
from epcomms.connection.transmission import Serial, TransmissionError
from epcomms.equipment.base import MeasurementError
from . import VacuumController

class Terranova962A(VacuumController):

    def __init__(self, device_location):
        transmission = Serial(device_location)
        super().__init__(transmission)

    def get_pressure_gauge_1(self) -> float:
        return self._get_pressure_gauge_n(0)
    
    def get_pressure_gauge_2(self) -> float:
        return self._get_pressure_gauge_n(1)
    
    def get_units(self) -> Union[Literal["Torr", "mBar"]]:
        unit_str = self.transmission.poll(ASCII('u')).data
        if unit_str in ["Torr", "mBar"]:
            return unit_str
        else:
            raise TransmissionError(f"Recieved a bad response: {unit_str} (expected unit)")
        
    def get_identity(self) -> str:
        ident_string = self.transmission.poll(ASCII('v')).data
        if "926" in ident_string:
            return ident_string
        else:
            raise TransmissionError(f"Recieved a bad response: {ident_string} (expected identity)")
        
    def get_gauge_type(self) -> Union[Literal["CEP", "275"]]:
        gauge_str = self.transmission.poll(ASCII('x')).data
        if gauge_str in ["CEP", "275"]:
            return gauge_str
        else:
            raise TransmissionError(f"Recieved a bad response: {gauge_str} (expected gauge type)")

    def _get_pressure_gauge_n(self, n: int) -> float:
        press_str = self.transmission.poll(ASCII('p')).data.strip().split(" ")[n]
        match press_str:
            case "Low":
                raise MeasurementError("Pressure out of range (low)")
            case "999e+0":
                raise MeasurementError("Pressure out of range (high)")
            case "Off":
                raise MeasurementError("Gauge off")
            case _:
                try:
                    return float(press_str)
                except ValueError:
                    print(press_str)
                    raise TransmissionError(f"Recieved a bad response: {press_str} (expected pressures)")

