import asyncio

import websockets

from epcomms.connection.packet import String

from .transmission import Transmission, TransmissionError


class Socket(Transmission[String, String]):
    """
    Socket transmission class using websockets.
    """

    def __init__(self, ws_url: str) -> None:
        super().__init__()
        self.ws_url = ws_url
        self._loop = asyncio.new_event_loop()

    async def _async_send(self, packet: String) -> None:
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(packet.serialize())

    def _command(self, packet: String) -> None:
        try:
            asyncio.run(self._async_send(packet))
        except Exception as e:
            raise TransmissionError(e) from e

    def _read(self) -> String:
        raise NotImplementedError

    async def _async_poll(self, packet: String) -> String:
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(packet.serialize())
            response = await websocket.recv()
            if not isinstance(response, str):
                raise TransmissionError("Received non-string response from socket.")
        return String.from_wire(response)

    def poll(self, packet: String) -> String:
        try:
            response = asyncio.run(self._async_poll(packet))
        except Exception as e:
            raise TransmissionError(e) from e

        return response
