from .client_methods import HighriseWebApiMethods
from aiorise.connection import BaseApiConnection
from aiorise.events.event_types import AnyEvent
from aiorise.events.event_wrapper import EventWrapper

from typing import AsyncIterable

class HighriseWebApiClient(HighriseWebApiMethods):
    _connection: BaseApiConnection

    def __init__(self, connection: BaseApiConnection):
        self._connection = connection


    async def connect(self) -> None:
        await self._connection.connect()

    async def listen(self) -> AsyncIterable[AnyEvent]:
        async for event in self._connection.listen(): # type: ignore
            yield EventWrapper.model_validate({'data': event}).data
            
