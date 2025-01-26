from epcomms.equipment.base import Instrument
from numpy import random


class TestInstrument(Instrument):
    def __init__(self):
        transmission = None
        super().__init__(transmission)

    def close(self) -> None:
        pass

    def get_noise(self) -> float:
        return random.normal(0, 1)

    def get_custom_noise(self, mean: float, std: float) -> float:
        return random.normal(mean, std)

    def echo(self, message: str) -> str:
        print(message)

    def echo_count(self, message: str, count: int) -> str:
        print(message * count)
