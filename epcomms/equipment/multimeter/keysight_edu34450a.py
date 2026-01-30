# TODO: This entire class should be refactored to use the be a SCPIMultimeter.

from typing import Union

from epcomms.connection.packet import String
from epcomms.connection.transmission import Visa

from .multimeter import Multimeter

# TODO: These are probably better as Literal types or something
# pylint: disable=invalid-name
RangeT = Union[str, int, float]
ResolutionT = str


class KeysightEDU34450A(Multimeter[Visa, RangeT, ResolutionT]):
    """
    A class to represent the Keysight EDU34450A multimeter.
    """

    def __init__(self, resource_name: str) -> None:
        """
        Initializes the Keysight EDU34450A multimeter.

        Args:
            resource_name (str): The VISA resource name of the multimeter.
        """
        transmission = Visa(resource_name, terminator="\n")
        super().__init__(transmission)

    def close(self) -> None:
        self.transmission.close()

    def beep(self) -> None:
        """
        Sends a command to the multimeter to emit a beep sound.
        """
        self.transmission.command(String.from_data("SYST:BEEP"))

    def measure_voltage_ac(
        self,
        measurement_range: RangeT = "AUTO",
        resolution: ResolutionT = "DEF",
    ) -> float:
        """Measures AC voltage using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a
                numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}.
                Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using
                autoranging (measurement_range == 'AUTO'), resolution must be
                set to 'DEF'. Defaults to 'DEF'.
            channel (str, optional): Only 'PRIMARY' channel works. Defaults to
                'PRIMARY'.

        Returns:
            float: The measured voltage value.
        """

        try:
            assert isinstance(
                measurement_range, (float, int)
            ) or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must be"
                " a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        try:
            assert resolution.upper() in {"DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of 'DEF'"
                ",'MAX','MIN'."
            ) from e

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                String.from_data(
                    f"MEASURE:PRIMARY:VOLTAGE:AC? {range_str},{resolution}"
                )
            ).deserialize()
        )

    def measure_voltage_dc(
        self,
        measurement_range: RangeT = "AUTO",
        resolution: ResolutionT = "DEF",
    ) -> float:

        try:
            assert isinstance(
                measurement_range, (float, int)
            ) or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must "
                "be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        try:
            assert resolution.upper() in {"DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of "
                "'DEF','MAX','MIN'."
            ) from e

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                String.from_data(
                    f"MEASURE:PRIMARY:VOLTAGE:DC? {range_str},{resolution}"
                )
            ).deserialize()
        )

    def measure_capacitance(
        self, measurement_range: RangeT = "AUTO", resolution: ResolutionT = "DEF"
    ) -> float:

        try:
            assert isinstance(
                measurement_range, (float, int)
            ) or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must "
                "be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        try:
            assert resolution.upper() in {"DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of "
                "'DEF','MAX','MIN'."
            ) from e

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                String.from_data(
                    f"MEASURE:PRIMARY:CAPACITANCE? {range_str},{resolution}"
                )
            ).deserialize()
        )

    def measure_continuity_raw(self) -> float:
        """Performs a 2-wire continuity test.

        Returns:
            float: A resistance reading, as returned by the instrument during
            continuity tests.
        """
        # TODO confirm return value when instrument sees an open circuit
        # (>1.2 kOhm). Programmer guide is unclear.
        return float(
            self.transmission.poll(
                String.from_data("MEASURE:PRIMARY:CONTINUITY?")
            ).deserialize()
        )

    def measure_continuity(self) -> bool:
        """Performs a 2-wire continuity test. The Keysight's internal threshold
          for continuity is 10 Ohms.

        Returns:
            bool: True if continuity is detected, otherwise false.
        """
        return self.measure_continuity_raw() <= 10.0

    def measure_current_ac(
        self,
        measurement_range: RangeT = "AUTO",
        resolution: ResolutionT = "DEF",
    ) -> float:
        try:
            assert isinstance(
                measurement_range, (float, int)
            ) or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must "
                "be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        try:
            assert resolution.upper() in {"DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of "
                "'DEF','MAX','MIN'."
            ) from e

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                String.from_data(
                    f"MEASURE:PRIMARY:CURRENT:AC? {range_str},{resolution}"
                )
            ).deserialize()
        )

    def measure_current_dc(
        self,
        measurement_range: RangeT = "AUTO",
        resolution: ResolutionT = "DEF",
    ) -> float:
        """Measures DC current using a specified measurement range, on a
        specified channel.

        Returns:
            float: The measured current value.
        """
        try:
            assert isinstance(
                measurement_range, (float, int)
            ) or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must "
                "be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        try:
            assert resolution.upper() in {"DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of "
                "'DEF','MAX','MIN'."
            ) from e

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                String.from_data(
                    f"MEASURE:PRIMARY:CURRENT:DC? {range_str},{resolution}"
                )
            ).deserialize()
        )

    def measure_diode(self) -> float:
        """Performs a diode test.

        Returns:
            float: A voltage reading, as returned by the instrument during
            diode tests, if the voltage is in the range [0,1.2]. If the signal
            is greater than 1.2V then the value +9.9e+37 is returned.
        """
        return float(
            self.transmission.poll(
                String.from_data("MEASURE:PRIMARY:DIODE?")
            ).deserialize()
        )

    def measure_frequency(
        self,
        measurement_range: RangeT = "DEF",
        resolution: ResolutionT = "DEF",
        amplitude_range: RangeT = 0.1,
    ) -> float:
        """Measures frequency of an AC volage signal at a desired resolution
        using a specified frequency range, on a specified channel.

        Before frequency measurement, the AC voltage range is configured. As
        per the programmer guide, the voltage range should be "at least" 0.1V
        for accurate frequency measurements.
        Returns:
            float: The measured current value.
        """
        try:
            assert isinstance(
                measurement_range, (float, int)
            ) or measurement_range.upper() in {
                "AUTO",
                "DEF",
                "MAX",
                "MIN",
            }
        except AssertionError as e:
            raise ValueError(
                "Invalid value for freq_range. Freq_range must be a numeric "
                "value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        try:
            assert resolution.upper() in {"DEF", "MAX", "MIN"}
        except AssertionError as e:
            raise ValueError(
                "Invalid value for freq_resolution. Resolution must be one of "
                "'DEF','MAX','MIN'."
            ) from e

        try:
            assert isinstance(
                amplitude_range, (float, int)
            ) or amplitude_range.upper() in {
                "AUTO",
                "DEF",
                "MAX",
                "MIN",
            }
        except AssertionError as e:
            raise ValueError(
                "Invalid value for volt_range. Volt_range must be a numeric "
                "value or one of 'AUTO','DEF','MAX','MIN'."
            ) from e

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        self.transmission.command(
            String.from_data(f"SENSE:PRIMARY:FREQUENCY:VOLTAGE:RANGE {amplitude_range}")
        )
        return float(
            self.transmission.poll(
                String.from_data(f"MEASURE:PRIMARY:FREQUENCY? {range_str},{resolution}")
            ).deserialize()
        )

    def read_errors(self):
        """Reads and prints all errors from the instrument error queue."""
        # TODO: WTF is this?? Return the errors instead.
        i = 0
        while True:
            err = self.transmission.poll(String.from_data("SYST:ERR?")).deserialize()
            print(err)
            i += 1
            if err == '+0, "No error"' or i >= 20:
                break
