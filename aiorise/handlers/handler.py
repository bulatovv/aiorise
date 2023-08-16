from typing import Self, Callable

from aiorise.actions.action import BaseAction
from aiorise.events.event_types import AnyEvent
from aiorise.events.event_context import EventContext
from aiorise.filters.filter import BaseFilter

import asyncio

class Handler:
    _parent: Self | None
    _children: list[Self]

    _filter: BaseFilter | None
    _action: BaseAction | None

    def __init__(self, parent: Self | None = None):
        self._parent = parent
        self._children = []
        self._filter = None
        self._action = None


    def add_child(self, child: Self) -> None:
        self._children.append(child)

    
    def set_filter(self, f: BaseFilter) -> None:
        self._filter = f


    def set_action(self, a: BaseAction) -> None:
        self._action = a

    def set(self, f: BaseFilter) -> Callable[[BaseAction], None]:
        def inner(a: BaseAction) -> None:
            self.set_filter(f)
            self.set_action(a)
        return inner

    def child(self, f: BaseFilter) -> Callable[[BaseAction], None]:
        def inner(a: BaseAction) -> None:
            child = Handler(self)
            child.set_filter(f)
            child.set_action(a)
            self.add_child(child)
        return inner


    async def run(self, e: AnyEvent, ctx: EventContext) -> None:
        if (await self._filter.check(e, ctx) if self._filter else True):
            await self._action.run(e, ctx) if self._action else None

            async with asyncio.TaskGroup() as tg:
                for child in self._children:
                    tg.create_task(child.run(e, ctx))
