from collections import defaultdict
from websockets.client import WebSocketClientProtocol
from typing import NoReturn, AsyncIterable
from abc import ABC, abstractmethod

import asyncio

import websockets.client
import websockets.exceptions

import json
import random


class BaseApiConnection(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def send(self, payload: dict, wait_for_resp: bool = True) -> dict:
        pass

    @abstractmethod
    async def listen(self) -> AsyncIterable[dict]:
        pass

class HighriseWebApiConnection(BaseApiConnection):
    _keepalive_timeout: int = 15
    _websocket: WebSocketClientProtocol
    _keepalive_task: asyncio.Task
    _requests: dict[str, asyncio.Future[dict]]
    
    uri: str
    api_token: str
    room_id: str


    def __init__(self, uri: str, api_token: str, room_id: str):
        self._requests = defaultdict(asyncio.Future)
        
        self.uri = uri
        self.api_token = api_token
        self.room_id = room_id


    async def _keepalive(self) -> NoReturn:
        while True:
            await asyncio.sleep(self._keepalive_timeout)
            await self.send({"_type": "KeepaliveRequest"})


    def _generate_rid(self) -> str:
        return random.randbytes(16).hex()


    async def connect(self) -> None:
        self._websocket = await websockets.client.connect(
            self.uri, 
            extra_headers={
                "api-token": self.api_token,
                "room-id": self.room_id
            }
        )

        session_metadata = await self._websocket.recv()

        self._keepalive_task = asyncio.create_task(self._keepalive()) 
   

    async def close(self) -> None:
        self._keepalive_task.cancel() 
        await self._websocket.close()  
 

    async def send(self, payload: dict, wait_for_resp: bool = True) -> dict:
        rid = self._generate_rid()
        payload["rid"] = rid
            
        print(payload)
        await self._websocket.send(json.dumps(payload))

        if wait_for_resp:
            result = await self._requests[rid]
            del self._requests[rid]
            return result
        else:
            return {}


    async def listen(self) -> AsyncIterable[dict]:
        async for message in self._websocket:
            try:
                message = json.loads(message)

                if rid := message.get("rid"):
                    self._requests[rid].set_result(message)
                else:
                    yield message

            except websockets.exceptions.ConnectionClosed:
                continue
