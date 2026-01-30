from epcomms.connection.packet import ASCII
from epcomms.connection.transmission import Serial, TransmissionError
from epcomms.equipment.base import MeasurementError

from .vacuum_controller import VacuumController


class Terranova962A(VacuumController[Serial[ASCII]]):
    """Terranova 962A Vacuum Controller implementation."""

    def __init__(self, device_location: str):
        transmission = Serial(device_location)
        super().__init__(transmission)

    def get_pressure_gauge_1(self) -> float:
        """
        Get the pressure reading from gauge 1.

        Returns:
            float: Pressure reading from gauge 1.
        """
        return self._get_pressure_gauge_n(0)

    def get_pressure_gauge_2(self) -> float:
        """
        Get the pressure reading from gauge 2.

        Returns:
            float: Pressure reading from gauge 2.
        """
        return self._get_pressure_gauge_n(1)

    def get_units(self) -> str:
        """
        Get the units of the pressure readings.
        """
        unit_str = self.transmission.poll(ASCII.from_data("u")).deserialize()
        return unit_str

    def get_identity(self) -> str:
        """
        Get the identity string of the device.
        """
        ident_string = self.transmission.poll(ASCII("v")).deserialize()
        if "926" in ident_string:
            return ident_string

        raise TransmissionError(
            f"Recieved a bad response: {ident_string} (expected identity)"
        )

    def get_gauge_type(self) -> str:
        """
        Get the type of pressure gauge connected.
        """
        gauge_str = self.transmission.poll(ASCII.from_data("x")).deserialize()
        if gauge_str in ["CEP", "275"]:
            return gauge_str

        raise TransmissionError(
            f"Recieved a bad response: {gauge_str} (expected gauge type)"
        )

    def _get_pressure_gauge_n(self, n: int) -> float:
        """
        Get the pressure reading from gauge n.
        """
        press_str = (
            self.transmission.poll(ASCII.from_data("p"))
            .deserialize()
            .strip()
            .split(" ")[n]
        )
        match press_str:
            case "Low":
                raise MeasurementError("Pressure out of range (low)")
            case "Hi":
                raise MeasurementError("Pressure out of range (high)")
            case "Off":
                raise MeasurementError("Gauge off")
            case _:
                try:
                    return float(press_str)
                except ValueError as e:
                    raise TransmissionError(
                        f"Recieved a bad response: {press_str} (expected pressures)"
                    ) from e
