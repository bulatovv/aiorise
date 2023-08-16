from pydantic import BaseModel
from .event_types import AnyEvent

class EventWrapper(BaseModel):
    data: AnyEvent
