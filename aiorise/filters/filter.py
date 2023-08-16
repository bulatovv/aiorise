from abc import ABC, abstractmethod
from typing import Callable, Awaitable, overload
from aiorise.events.event_types import AnyEvent
from aiorise.events.event_context import EventContext

import asyncio


class BaseFilter(ABC):
    @abstractmethod
    async def check(self, e: AnyEvent, ctx: EventContext) -> bool:
        pass


class SyncFilter(BaseFilter):
    _func: Callable[[AnyEvent, EventContext], bool]

    def __init__(self, func: Callable[[AnyEvent, EventContext], bool]):
        self._func = func

    async def check(self, e: AnyEvent, ctx: EventContext) -> bool:
        return self._func(e, ctx)


class AsyncFilter(BaseFilter):
    _afunc: Callable[[AnyEvent, EventContext], Awaitable[bool]]

    def __init__(self, afunc: Callable[[AnyEvent, EventContext], Awaitable[bool]]):
        self._afunc = afunc

    async def check(self, e: AnyEvent, ctx: EventContext) -> bool:
        return await self._afunc(e, ctx)


class FilterFactory:
    SupportedTypes = (
        BaseFilter
        | Callable[[AnyEvent, EventContext], bool]
        | Callable[[AnyEvent, EventContext], Awaitable[bool]]
    )

    @overload
    @staticmethod
    def create(f: BaseFilter) -> BaseFilter:
        pass

    @overload
    @staticmethod
    def create(f: Callable[[AnyEvent, EventContext], bool]) -> BaseFilter:
        pass

    @overload
    @staticmethod
    def create(f: Callable[[AnyEvent, EventContext], Awaitable[bool]]) -> BaseFilter:
        pass

    @staticmethod
    def create(f):
        if isinstance(f, BaseFilter):
            return f
        elif callable(f):
            if asyncio.iscoroutinefunction(f):
                return AsyncFilter(f)
            else:
                return SyncFilter(f)
        else:
            raise TypeError(f"Invalid type for filter {type(f)}")
