# pylint: disable=duplicate-code
from abc import abstractmethod
from typing import Generic, TypeVar

from epcomms.equipment.base import Instrument, TransmissionTypeT

RangeT = TypeVar("RangeT")
ResolutionT = TypeVar("ResolutionT")


class Multimeter(
    Instrument[TransmissionTypeT],
    Generic[TransmissionTypeT, RangeT, ResolutionT],
):
    """Abstract class for all multimeters."""

    @abstractmethod
    def measure_voltage_ac(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """
        Measure an AC voltage

        Args:
            measurement_range (RangeT, optional): measurement range for this
                measurement. Defaults to None.
            resolution (ResolutionT, optional): resolution for this
                measurement. Defaults to None.


        Returns:
            float: the measured AC voltage
        """
        raise NotImplementedError

    @abstractmethod
    def measure_voltage_dc(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """
        Measure a DC voltage

        Args:
            measurement_range (RangeT, optional): measurement range for this
                measurement. Defaults to None.
            resolution (ResolutionT, optional): resolution for this
                measurement. Defaults to None.

        Returns:
            float: the measured DC voltage
        """
        raise NotImplementedError

    @abstractmethod
    def measure_capacitance(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """_summary_

        Args:
            measurement_range (RangeT, optional): measurement range for this
                measurement. Defaults to None.
            resolution (ResolutionT, optional): resolution for this
                measurement. Defaults to None.

        Returns:
            float: the measured capacitance
        """
        raise NotImplementedError

    @abstractmethod
    def measure_continuity(self) -> bool:
        """
        Use the multimeter to check if a circuit has continuity.

        Returns:
            bool: True if circuit is continuous.
        """
        raise NotImplementedError

    @abstractmethod
    def measure_current_ac(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """
        Measure an AC current

        Args:
            measurement_range (RangeT, optional): measurement range for this
                measurement. Defaults to None.
            resolution (ResolutionT, optional): resolution for this
                measurement. Defaults to None.


        Returns:
            float: the measured AC current
        """
        raise NotImplementedError

    @abstractmethod
    def measure_current_dc(
        self,
        measurement_range: RangeT = None,
        resolution: ResolutionT = None,
    ) -> float:
        """_summary_

        Args:
            measurement_range (RangeT, optional): measurement range for this
                measurement. Defaults to None.
            resolution (ResolutionT, optional): resolution for this
                measurement. Defaults to None.

        Returns:
            float: the measured DC current
        """
        raise NotImplementedError
