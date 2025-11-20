from typing import TypeVar, Union

from epcomms.connection.packet import ASCII, String
from epcomms.connection.transmission import Transmission
from epcomms.equipment.base import SCPIInstrument

PacketT = TypeVar("PacketT", ASCII, String)

from .multimeter import Multimeter

RangeT = Union[str, int, float, None]
ResolutionT = Union[str, None]


class SCPIMultimeter(
    Multimeter[Transmission[PacketT, PacketT], RangeT, ResolutionT], SCPIInstrument
):
    """
    A class to represent a generic SCPI multimeter.
    """

    def __init__(
        self, transmission: Transmission[PacketT, PacketT], packet: type[PacketT]
    ) -> None:
        super().__init__(transmission)
        self._packet = packet

    def beep(self) -> None:
        """
        Sends a command to the multimeter to emit a beep sound.

        This method uses the transmission interface to send the "SYST:BEEP"
        command to the connected Keysight EDU34450A multimeter, causing it
        to produce an audible beep.

        Returns:
            None
        """
        self.transmission.command(self._packet.from_data("SYST:BEEP"))

    def measure_voltage_ac(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """Measures AC voltage using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using auto-ranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured voltage value.
        """

        if measurement_range is None:
            measurement_range = "AUTO"
        if resolution is None:
            resolution = "DEF"

        if not (
            isinstance(measurement_range, (float, int))
            or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        ):
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )
        elif not (resolution.upper() in {"DEF", "MAX", "MIN"}):
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'."
            )

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                self._packet.from_data(
                    self.generate_query(
                        "MEAS:VOLT:AC", arguments=[range_str, resolution]
                    )
                )
            ).deserialize()
        )

    def measure_voltage_dc(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """Measures DC voltage using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Volts), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using auto-ranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured voltage value.
        """

        if measurement_range is None:
            measurement_range = "AUTO"
        if resolution is None:
            resolution = "DEF"

        if not (
            isinstance(measurement_range, (float, int))
            or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        ):
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )

        elif not (resolution.upper() in {"DEF", "MAX", "MIN"}):
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'."
            )

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                self._packet.from_data(
                    self.generate_query(
                        "MEAS:VOLT:DC", arguments=[range_str, resolution]
                    )
                )
            ).deserialize()
        )

    def measure_capacitance(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """Measures capacitance using a specified measurement range, on the 'PRIMARY' channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Farads), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using auto-ranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured capacitance value.
        """

        if measurement_range is None:
            measurement_range = "AUTO"
        if resolution is None:
            resolution = "DEF"

        if not (
            isinstance(measurement_range, (float, int))
            or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        ):
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )

        elif not (resolution.upper() in {"DEF", "MAX", "MIN"}):
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'."
            )

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                self._packet.from_data(
                    self.generate_query("MEAS:CAP", arguments=[range_str, resolution])
                )
            ).deserialize()
        )

    def measure_continuity_raw(self) -> float:
        """Performs a 2-wire continuity test.

        Returns:
            float: A resistance reading, as returned by the instrument during continuity tests.
        """
        # TODO confirm return value when instrument sees an open circuit (>1.2 kOhm). Programmer guide is unclear.
        return float(
            self.transmission.poll(
                self._packet.from_data(self.generate_query("MEAS:CONT"))
            ).deserialize()
        )

    def measure_continuity(self) -> bool:
        """Performs a 2-wire continuity test. The Keysight's internal threshold for continuity is 10 Ohms.

        Returns:
            bool: True if continuity is detected, otherwise false.
        """
        return self.measure_continuity_raw() <= 10.0

    def measure_current_ac(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """Measures AC current using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using auto-ranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured current value.
        """

        if measurement_range is None:
            measurement_range = "AUTO"
        if resolution is None:
            resolution = "DEF"

        if not (
            isinstance(measurement_range, (float, int))
            or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        ):
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )
        elif not (resolution.upper() in {"DEF", "MAX", "MIN"}):
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'."
            )

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                self._packet.from_data(
                    self.generate_query(
                        "MEAS:CURR:AC", arguments=[range_str, resolution]
                    )
                )
            ).deserialize()
        )

    def measure_current_dc(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """Measures DC current using a specified measurement range, on a specified channel.

        Args:
            measurement_range (Union[str | int | float], optional): Specify a numeric value (in Amps), or one of {AUTO|DEF|MAX|MIN}. Defaults to 'AUTO'.
            resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using autoranging (measurement_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.

        Returns:
            float: The measured current value.
        """

        if measurement_range is None:
            measurement_range = "AUTO"
        if resolution is None:
            resolution = "DEF"

        if not (
            isinstance(measurement_range, (float, int))
            or measurement_range.upper() in {"AUTO", "DEF", "MAX", "MIN"}
        ):
            raise ValueError(
                "Invalid value for measurement_range. Measurement_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )

        elif not (resolution.upper() in {"DEF", "MAX", "MIN"}):
            raise ValueError(
                "Invalid value for resolution. Resolution must be one of 'DEF','MAX','MIN'."
            )

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        return float(
            self.transmission.poll(
                self._packet.from_data(
                    self.generate_query(
                        "MEAS:CURR:DC", arguments=[range_str, resolution]
                    )
                )
            ).deserialize()
        )

    def measure_frequency(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
        amplitude_range: RangeT = None,
    ) -> float:
        """Measures frequency of an AC volage signal at a desired resolution using a specified frequency range, on a specified channel.

        Before frequency measurement, the AC voltage range is configured. As per the programmer guide, the voltage range should be "at least" 0.1V for accurate frequency measurements.

        Args:
            freq_range (Union[str | int | float], optional): Specify a numeric value (in Hz), or one of {DEF|MAX|MIN}. MIN = DEF = 1 Hz, MAX = 1 MHz. Defaults to 'DEF'.
            freq_resolution (str, optional): Specify one of {DEF|MAX|MIN}. If using auto-ranging (freq_range == 'AUTO'), resolution must be set to 'DEF'. Defaults to 'DEF'.
            volt_range (Union[str | int | float], optional): Specify a numeric value (in V), or one of {AUTO|DEF|MAX|MIN}. Defaults to 0.1 V.

        Returns:
            float: The measured current value.
        """

        if measurement_range is None:
            measurement_range = "AUTO"
        if resolution is None:
            resolution = "DEF"
        if amplitude_range is None:
            amplitude_range = 0.1

        if not (
            isinstance(measurement_range, (float, int))
            or measurement_range.upper()
            in {
                "AUTO",
                "DEF",
                "MAX",
                "MIN",
            }
        ):
            raise ValueError(
                "Invalid value for freq_range. Freq_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )
        elif not resolution.upper() in {"DEF", "MAX", "MIN"}:
            raise ValueError(
                "Invalid value for freq_resolution. Resolution must be one of 'DEF','MAX','MIN'."
            )

        elif not (
            isinstance(amplitude_range, (float, int))
            or amplitude_range.upper()
            in {
                "AUTO",
                "DEF",
                "MAX",
                "MIN",
            }
        ):
            raise ValueError(
                "Invalid value for volt_range. Volt_range must be a numeric value or one of 'AUTO','DEF','MAX','MIN'."
            )

        range_str = (
            measurement_range
            if isinstance(measurement_range, str)
            else f"{measurement_range:.2e}"
        )
        self.transmission.command(
            self._packet.from_data(
                self.generate_command(
                    "SENS:FREQ:VOLT:RANGE", arguments=str(amplitude_range)
                )
            )
        )
        return float(
            self.transmission.poll(
                self._packet.from_data(
                    self.generate_query(
                        "MEASURE:FREQUENCY", arguments=[range_str, resolution]
                    )
                )
            ).deserialize()
        )

    def read_errors(self):
        # TODO c'mon. Really? Return the errors instead.
        i = 0
        while True:
            err = self.transmission.poll(
                self._packet.from_data("SYST:ERR?")
            ).deserialize()
            print(err)
            i += 1
            if err == '+0, "No error"' or i >= 20:
                break
