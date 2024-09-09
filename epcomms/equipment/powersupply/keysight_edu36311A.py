from . import PowerSupply
from epcomms.connection.transmission import Visa


class KeysightEDU36311A(PowerSupply):

    def __init__(self, resource_name) -> None:
        transmission = Visa(resource_name)
        super().__init__(transmission)

    def beep(self) -> None:
        self.transmission.command("SYST:BEEP")

    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        self.transmission.command(f"VOLT {voltage},(@{channel})")

    def measure_voltage(self, channel: int = 0) -> float:
        return float(self.transmission.poll(f"MEAS:VOLT? (@{channel})"))

    def set_current(self, current: float, channel: int = 0) -> None:
        self.transmission.command(f"CURR {current},(@{channel})")

    def measure_current(self, channel: int = 0) -> float:
        return float(self.transmission.poll(f"MEAS:CURR? (@{channel})"))

    def enable_output(self, channel: int = 0) -> None:
        self.transmission.command(f"OUTP 1,(@{channel})")

    def disable_output(self, channel: int = 0) -> None:
        self.transmission.command(f"OUTP 0,(@{channel})")
