from abc import abstractmethod

from epcomms.equipment.base import Instrument, TransmissionTypeT


class TemperatureSensor(Instrument[TransmissionTypeT]):
    """Abstract Base Class for all Power Supplies."""

    @abstractmethod
    def configure_channel(self, channel: int, channel_type: str) -> None:
        """Configure a channel on the temperature sensor for a given
        thermocouple type."""
        raise NotImplementedError

    @abstractmethod
    def disable_channel(self, channel: int) -> None:
        """Disable a channel on the temperature sensor."""
        raise NotImplementedError

    @abstractmethod
    def measure_temperature(self, channel: int) -> float:
        """Measure the temperature from a specific channel."""
        raise NotImplementedError
