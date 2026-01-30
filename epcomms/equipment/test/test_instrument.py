from numpy import random

from epcomms.equipment.base import Instrument


class TestInstrument(Instrument[None]):
    """A test instrument for demonstration and development"""

    def __init__(self):
        transmission = None
        super().__init__(transmission)

    def close(self) -> None:
        pass

    def get_noise(self) -> float:
        """
        Get a random noise value.

        Returns:
            float: A random noise value from a normal distribution with mean 0 and std 1.
        """
        return random.normal(0, 1)

    def get_custom_noise(self, mean: float, std: float) -> float:
        """
        Get a random noise value with custom mean and standard deviation.

        Args:
            mean (float): mean of the normal distribution
            std (float): standard deviation of the normal distribution

        Returns:
            float: A random noise value from a normal distribution with specified mean and std.
        """
        return random.normal(mean, std)

    def echo(self, message: str) -> None:
        """
        Echoes the provided message.

        Args:
            message (str): The message to echo.
        """
        print(message)

    def echo_count(self, message: str, count: int) -> None:
        """
        Echoes the provided message a specified number of times.

        Args:
            message (str): The message to echo.
            count (int): The number of times to echo the message.
        """
        print(message * count)
