from . import PowerSupply
from epcomms.connection.transmission import Visa
from epcomms.connection.packet import ASCII


class KeysightEDU36311A(PowerSupply):

    def __init__(self, resource_name) -> None:
        transmission = Visa(resource_name)
        super().__init__(transmission)

    def beep(self) -> None:
        self.transmission.command(ASCII("SYST:BEEP"))

    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        self.transmission.command(ASCII(f"VOLT {voltage},(@{channel})"))

    def measure_voltage(self, channel: int = 0) -> float:
        return float(self.transmission.poll(ASCII(f"MEAS:VOLT? (@{channel})")).data)

    def set_current(self, current: float, channel: int = 0) -> None:
        self.transmission.command(ASCII(f"CURR {current},(@{channel})"))

    def measure_current(self, channel: int = 0) -> float:
        return float(self.transmission.poll(ASCII(f"MEAS:CURR? (@{channel})")).data)

    def enable_output(self, channel: int = 0) -> None:
        self.transmission.command(ASCII(f"OUTP 1,(@{channel})"))

    def disable_output(self, channel: int = 0) -> None:
        self.transmission.command(ASCII(f"OUTP 0,(@{channel})"))
