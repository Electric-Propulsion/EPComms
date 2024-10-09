# pylint: disable=missing-module-docstring
# TODO: add module docstring # pylint: disable=fixme
from abc import abstractmethod
from epcomms.equipment.base import Instrument


class DAQ(Instrument):
    # pylint: disable=missing-class-docstring
    # pylint: disable=too-few-public-methods
    
    @abstractmethod
    def measure_voltage(self, channel: int) -> float:
        """Perform a single, untriggered voltage measurement."""
        raise NotImplementedError
    
    @abstractmethod
    def configure_daq_channel(self, channel: int, voltage_range: float, offset_voltage: float) -> None:
        """Configures a channel of an instrument as a DAQ."""
        raise NotImplementedError
