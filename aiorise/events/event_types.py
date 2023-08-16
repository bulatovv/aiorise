from pydantic import BaseModel, Field
from typing import Literal, Any
from aiorise.objects.object_types import *


class ChatEvent(BaseModel):
    """A chat event, sent by a `user` in the room."""

    type: Literal["ChatEvent"] = Field(alias="_type")
    user: User
    message: str
    whisper: bool


class EmoteEvent(BaseModel):
    """An emote event, performed by a `user` in the room."""

    type: Literal["EmoteEvent"] = Field(alias="_type")
    user: User
    emote_id: str
    receiver: User


class ReactionEvent(BaseModel):
    """A reaction event, performed by a `user` in the room."""

    type: Literal["ReactionEvent"] = Field(alias="_type")
    user: User
    reaction: Literal["clap", "heart", "thumbs", "wave", "wink"]
    receiver: User


class UserJoinedEvent(BaseModel):
    """A user has joined the room."""

    type: Literal["UserJoinedEvent"] = Field(alias="_type")
    user: User
    position: Position | AnchorPosition


class UserLeftEvent(BaseModel):
    """A user has left the room."""

    type: Literal["UserLeftEvent"] = Field(alias="_type")
    user: User


class ChannelEvent(BaseModel):
    """A hidden channel event."""

    type: Literal["ChannelEvent"] = Field(alias="_type")
    sender_id: str
    msg: str
    tags: list[str] | None = None


class TipReactionEvent(BaseModel):
    """The `sender` has sent `receiver` a tip (the `item`) in the current room."""

    type: Literal["TipReactionEvent"] = Field(alias="_type")
    sender: User
    receiver: User
    item: Item | CurrencyItem


class UserMovedEvent(BaseModel):
    """A user has moved in the room."""

    type: Literal["UserMovedEvent"] = Field(alias="_type")
    user: User
    position: Position | AnchorPosition


class VoiceEvent(BaseModel):
    """Event that is sent when status of voice is changed in the room.

    users: The list of users that currently have voice chat privileges in the room and status of their voice.
    seconds_left: The number of seconds left until the voice chat ends."""

    type: Literal["VoiceEvent"] = Field(alias="_type")
    users: list[tuple[User, Any]]
    seconds_left: int


class MessageEvent(BaseModel):
    """A message event, indicating that bot has received a message from someone. If the message is from a new conversation,
    `is_new_conversation` field will be True."""

    type: Literal["MessageEvent"] = Field(alias="_type")
    user_id: str
    conversation_id: str
    is_new_conversation: bool


AnyEvent = (
    ChatEvent
    | EmoteEvent
    | ReactionEvent
    | UserJoinedEvent
    | UserLeftEvent
    | ChannelEvent
    | TipReactionEvent
    | UserMovedEvent
    | VoiceEvent
    | MessageEvent
)
