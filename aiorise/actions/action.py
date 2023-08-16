from abc import ABC, abstractmethod
from typing import Callable, Awaitable, overload
from aiorise.events.event_types import AnyEvent
from aiorise.events.event_context import EventContext

import asyncio

class BaseAction(ABC):
    @abstractmethod
    async def run(self, e: AnyEvent, ctx: EventContext) -> None:
        pass


class SyncAction(BaseAction):
    _func: Callable[[AnyEvent, EventContext], None]

    def __init__(self, func: Callable[[AnyEvent, EventContext], None]):
        self._func = func

    async def run(self, e: AnyEvent, ctx: EventContext) -> None:
        self._func(e, ctx)


class AsyncAction(BaseAction):
    _afunc: Callable[[AnyEvent, EventContext], Awaitable[None]]

    def __init__(self, afunc: Callable[[AnyEvent, EventContext], Awaitable[None]]):
        self._afunc = afunc

    async def run(self, e: AnyEvent, ctx: EventContext) -> None:
        await self._afunc(e, ctx)


class ActionFactory:
    SupportedTypes = (
        BaseAction
        | Callable[[AnyEvent, EventContext], None]
        | Callable[[AnyEvent, EventContext], Awaitable[None]]
    )

    @overload
    @staticmethod
    def create(a: BaseAction) -> BaseAction:
        pass

    @overload
    @staticmethod
    def create(a: Callable[[AnyEvent, EventContext], None]) -> BaseAction:
        pass

    @overload
    @staticmethod
    def create(a: Callable[[AnyEvent, EventContext], Awaitable[None]]) -> BaseAction:
        pass

    @staticmethod
    def create(a):
        if isinstance(a, BaseAction):
            return a
        elif callable(a):
            if asyncio.iscoroutinefunction(a):
                return AsyncAction(a)
            else:
                return SyncAction(a)
        else:
            raise TypeError(f"Invalid type for action {type(a)}")
