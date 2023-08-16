from typing import Protocol
from aiorise.connection import BaseApiConnection

class HaveApiConnection(Protocol):
    @property
    def _connection(self) -> BaseApiConnection: ...
