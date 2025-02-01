"""
BK1694 Power Supply Control over ESP32
This module provides an interface to control the BK1694 power supply by sending commands to a server hosted on an ESP32.
See https://github.com/Electric-Propulsion/BK1694_Controller.
"""

from epcomms.connection.transmission.sockets import Socket 

class BK1694():

    def __init__(self, ip: str):
        self.ip = ip # Ours is "192.168.0.156"
        self.ws_url = f"ws://{self.ip}:7777"
        self.socket = Socket(self.ws_url)

    async def set_voltage(self, voltage: float) -> dict:
        """Set the voltage.

        Args:
            voltage (float): For the BK1694, a float between 0 and 30 V.
                Will be accurate to the ± 0.12 V because the user-provided
                voltage is mapped to an integer between 0-255.
        """
        data = {
            "command": "setValue",
            "value": int(voltage*255/30)
        }
        response = self.socket.poll(data)
        return response

    async def get_status(self) -> dict:
        """Gets system status.

        Returns:
            dict: Response from ESP32 server.
        """
        data = {
            "command": "getStatus"
        }
        response = self.socket.poll(data)
        return response
    
    async def enable(self, state: bool) -> dict:
        """Enables or disables the power supply.

        Args:
            state (bool): True to enable, False to disable.

        Returns:
            dict: Response from ESP32 server.
        """
        data = {
            "command": "enable",
            "value": state
        }
        response = self.socket.poll(data)
        return response