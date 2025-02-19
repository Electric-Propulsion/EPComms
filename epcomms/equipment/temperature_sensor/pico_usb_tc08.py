"""
Pico USB-TC-08 Thermocouple DAQ control.
This module provides an interface to control the Pico USB-TC-08.
"""

from epcomms.connection.transmission.sockets import Socket

from . import TemperatureSensor

class PicoUSBTC08(TemperatureSensor):

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.ws_url = f"ws://{self.ip}:{str(self.port)}"
        self.transmission = Socket(self.ws_url)

    def open_instrument(self) -> None:
        data = {"command": "open_instrument"}
        self.transmission.command(data)
    
    def close_instrument(self) -> None:
        data = {"command": "close_instrument"}
        self.transmission.command(data)

    def enable_sampling(self, sampling_interval: int) -> None:
        data = {"command": "enable_sampling", "sampling_interval": sampling_interval}
        self.transmission.command(data)
    
    def disable_sampling(self) -> None:
        data = {"command": "disable_sampling"}
        self.transmission.command(data)

    def configure_channel(self, channel: int, type: str) -> None:
        data = {"command": "configure_channel", "channel": channel, "type": type}
        self.transmission.command(data)
    
    def disable_channel(self, channel: int) -> None:
        data = {"command": "disable_channel", "channel": int}
        self.transmission.command(data)
    
    def measure_temperature(self, channel: int) -> float:
        raise NotImplementedError("The Pico USB TC-08 does not support measuring temperature from one channel at a time.")
    
    def measure_all_channels(self) -> dict:
        data = {"command": "measure_all_channels"}
        return self.transmission.poll(data)