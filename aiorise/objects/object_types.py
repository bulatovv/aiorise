from pydantic import BaseModel, Field
from typing import Literal, Any


class Item(BaseModel):
    """A Highrise item."""

    type: Literal["clothing", "collectible"]
    amount: int
    id: str
    account_bound: bool
    active_palette: int | None = None


class User(BaseModel):
    """A Highrise user.

    Keep in mind it's possible for users to change their username,
    but their ID will never change."""

    id: str
    username: str


class Message(BaseModel):
    message_id: str
    conversation_id: str
    content: str
    sender_id: str
    category: Literal["text", "invite"]


class Conversation(BaseModel):
    id: str
    did_join: bool
    unread_count: int
    muted: bool
    member_ids: list[str] | None = None
    name: str | None = None
    owner_id: str | None = None


class Position(BaseModel):
    x: float
    y: float
    z: float
    facing: Literal["FrontRight", "FrontLeft", "BackRight", "BackLeft"] | None = None


class AnchorPosition(BaseModel):
    entity_id: str
    anchor_ix: int


class RoomInfo(BaseModel):
    """Information about the room."""

    owner_id: str
    room_name: str


class CurrencyItem(BaseModel):
    """A Highrise currency amount.

    The most used currencies are:
    * `gold`
    * `bubbles`

    Many other currencies exist, however."""

    type: str
    amount: int
