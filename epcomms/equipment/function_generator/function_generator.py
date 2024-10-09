from enum import Enum
from abc import abstractmethod
from epcomms.equipment.base import Instrument

class FunctionGeneratorMode(Enum):
    DC = 0
    SINE = 1
    SQUARE = 2
    TRIANGLE = 3
    RAMP_UP = 4
    RAMP_DOWN = 5
    NOISE = 6



class FunctionGenerator(Instrument):
    @abstractmethod
    def set_mode(self, mode: FunctionGeneratorMode, channel: int) -> None:
        """Sets the mode of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def get_mode(self, channel: int) -> FunctionGeneratorMode:
        """Gets the mode of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def set_frequency(self, frequency: float, channel: int) -> None:
        """Sets the frequency of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def get_frequency(self, channel: int) -> float:
        """Gets the frequency of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def set_amplitude(self, amplitude: float, channel: int) -> None:
        """Sets the amplitude of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def get_amplitude(self, channel: int) -> float:
        """Gets the amplitude of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def set_offset(self, offset: float, channel: int) -> None:
        """Sets the offset of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def get_offset(self, channel: int) -> float:
        """Gets the offset of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def set_duty_cycle(self, duty_cycle: float, channel: int) -> None:
        """Sets the duty cycle of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def get_duty_cycle(self, channel: int) -> float:
        """Gets the duty cycle of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def set_phase(self, phase: float, channel: int) -> None:
        """Sets the phase of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def get_phase(self, channel: int) -> float:
        """Gets the phase of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def start_output(self, channel: int, repeat: bool) -> None:
        """Enables the output of the function generator."""
        raise NotImplementedError
    
    @abstractmethod
    def disable_output(self, channel: int) -> None:
        """Disables the output of the function generator."""
        raise NotImplementedError
    
    @property
    @abstractmethod
    def channels(self) -> int:
        """Returns the number of channels on the function generator."""
        raise NotImplementedError

    

    
