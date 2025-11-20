"""
Pico USB-TC-08 Thermocouple DAQ control.
This module provides an interface to control the Pico USB-TC-08.
"""

import json

from epcomms.connection.packet import String
from epcomms.connection.transmission import Socket

from . import TemperatureSensor


class PicoUSBTC08(TemperatureSensor[Socket]):

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.ws_url = f"ws://{self.ip}:{str(self.port)}"
        self.transmission = Socket(self.ws_url)

        self.open_instrument()

    def open_instrument(self) -> None:
        """
        Starts the Pico Datalogger and automatically configures all 8 channels to be of 'K' type.
        """
        data = json.dumps({"command": "open_instrument"})
        self.transmission.command(String.from_data(data))

    def close_instrument(self) -> None:
        data = json.dumps({"command": "close_instrument"})
        self.transmission.command(String.from_data(data))

    def configure_channel(self, channel: int, channel_type: str) -> None:
        data = json.dumps(
            {"command": "configure_channel", "channel": channel, "type": channel_type}
        )
        self.transmission.command(String.from_data(data))

    def disable_channel(self, channel: int) -> None:
        """
        DO NOT DISABLE CHANNELS, EPComms will crash.
        """
        data = json.dumps({"command": "disable_channel", "channel": channel})
        self.transmission.command(String.from_data(data))

    def measure_temperature(self, channel: int) -> float:
        raise NotImplementedError(
            "The Pico USB TC-08 does not support measuring temperature from one channel at a time."
        )

    def measure_all_channels(self) -> list[float]:
        data = json.dumps({"command": "measure_all_channels"})
        resp = self.transmission.poll(String.from_data(data)).deserialize()
        # For some reason websockets sends JSON strings with single quotes (bad).
        resp_unp = json.loads(str(resp).replace("'", '"'))
        # Return all real channels (not cold junction), hence index 0 excluded.
        return [float(val) for val in resp_unp["temps"][1:]]
