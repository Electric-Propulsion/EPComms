"""_summary_

Returns:
    _type_: _description_
"""

import asyncio
import websockets
import json

from . import Transmission, TransmissionError


class Socket(Transmission):

    def __init__(self, ws_url: str) -> None:
        super().__init__(packet_class=dict)
        self.ws_url = ws_url
        self._loop = asyncio.new_event_loop()

    async def _async_send(self, data:dict) -> None:
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(json.dumps(data))

    def command(self, data: dict) -> None:
        try:
            asyncio.run(self._async_send(data))
        except Exception as e:
            raise TransmissionError(e) from e

    def _command(self, data: dict) -> None:
        raise NotImplementedError

    def _read(self) -> dict:
        raise NotImplementedError

    async def _async_poll(self, data: dict) -> dict:
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(json.dumps(data))
            response = await websocket.recv()
        return response

    def poll(self, data: dict) -> dict:
        try:
            response = json.loads(asyncio.run(
                self._async_poll(data)
            ))
        except Exception as e:
            raise TransmissionError(e) from e

        return response
