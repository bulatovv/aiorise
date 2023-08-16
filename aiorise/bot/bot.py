from aiorise.actions.action import ActionFactory
from aiorise.api.client import HighriseWebApiClient
from aiorise.handlers.handler import Handler
from aiorise.events.event_context import EventContext

from typing import NoReturn

class Bot:
    _client: HighriseWebApiClient
    _handler: Handler

    def __init__(self, client: HighriseWebApiClient, handler: Handler):
        self._client = client
        self._handler = handler

    async def start(self) -> NoReturn:
        await self._client.connect()

        async for event in self._client.listen():
            await self._handler.run(event, EventContext(client=self._client))
