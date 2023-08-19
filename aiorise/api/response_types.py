from pydantic import BaseModel, Field
from typing import Literal, Any
from aiorise.objects.object_types import *


class EmoteResponse(BaseModel):
    """The successful response to a `EmoteRequest`."""

    type: Literal["EmoteResponse"] = Field(alias="_type")


class ChannelResponse(BaseModel):
    """A channel message has been successfully sent."""

    type: Literal["ChannelResponse"] = Field(alias="_type")


class GetRoomUsersResponse(BaseModel):
    """The list of users in the room, alongside their positions."""

    type: Literal["GetRoomUsersResponse"] = Field(alias="_type")
    content: list[tuple[User, Position | AnchorPosition]]


class ReactionResponse(BaseModel):
    """A response to a successful reaction."""

    type: Literal["ReactionResponse"] = Field(alias="_type")


class GetWalletResponse(BaseModel):
    """The bot's wallet."""

    type: Literal["GetWalletResponse"] = Field(alias="_type")
    content: list[CurrencyItem]


class TeleportResponse(BaseModel):
    """The successful response to a `TeleportRequest`."""

    type: Literal["TeleportResponse"] = Field(alias="_type")


class FloorHitResponse(BaseModel):
    """The successful response to a `FloorHitRequest`."""

    type: Literal["FloorHitResponse"] = Field(alias="_type")


class AnchorHitResponse(BaseModel):
    """The successful response to a `AnchorHitRequest`."""

    type: Literal["AnchorHitResponse"] = Field(alias="_type")


class KeepaliveResponse(BaseModel):
    """The successful response to a `KeepaliveRequest`."""

    type: Literal["KeepaliveResponse"] = Field(alias="_type")


class ModerateRoomResponse(BaseModel):
    """The successful response to a `ModerateRoomRequest`."""

    type: Literal["ModerateRoomResponse"] = Field(alias="_type")


class GetRoomPrivilegeResponse(BaseModel):
    """The room privileges for provided `user_id`."""

    type: Literal["GetRoomPrivilegeResponse"] = Field(alias="_type")


class ChangeRoomPrivilegeResponse(BaseModel):
    """The successful response to a `ChangeRoomPrivilegeRequest`."""

    type: Literal["ChangeRoomPrivilegeResponse"] = Field(alias="_type")


class MoveUserToRoomResponse(BaseModel):
    """The successful response to a `MoveUserToRoomRequest`."""

    type: Literal["MoveUserToRoomResponse"] = Field(alias="_type")


class CheckVoiceChatResponse(BaseModel):
    """Returns the status of voice chat in the room.
    seconds_left: The number of seconds left until the voice chat ends.
    auto_speakers: The list of users that automatically have voice chat privileges in the room like moderators and
    owner.
    users: The list of users that currently have voice chat privileges in the room."""

    type: Literal["CheckVoiceChatResponse"] = Field(alias="_type")
    seconds_left: int


class GetUserOutfitResponse(BaseModel):
    """The outfit of a user. Returns list of items user is currently wearing."""

    type: Literal["GetUserOutfitResponse"] = Field(alias="_type")
    outfit: list[Item]


class GetMessagesResponse(BaseModel):
    """The messages of a conversation. This will return list of max 20 messages."""

    type: Literal["GetMessagesResponse"] = Field(alias="_type")
    messages: list[Message]


class SendMessageResponse(BaseModel):
    """The message sent success response."""

    type: Literal["SendMessageResponse"] = Field(alias="_type")


class GetConversationsResponse(BaseModel):
    """The conversations of a bot. This will return list of max 20 conversations.
    not_joined: The number of conversations that bot has not joined yet. Those are not returned in the conversations
    list unless not_joined is true."""

    type: Literal["GetConversationsResponse"] = Field(alias="_type")
    conversations: list[Conversation]
    not_joined: int


class LeaveConversationResponse(BaseModel):
    """The leave conversation success response."""

    type: Literal["LeaveConversationResponse"] = Field(alias="_type")


class BuyVoiceTimeResponse(BaseModel):
    """Buy a voice token."""

    type: Literal["BuyVoiceTimeResponse"] = Field(alias="_type")
    result: Literal["success", "insufficient_funds", "only_token_bought"]


class BuyRoomBoostResponse(BaseModel):
    """Buy a room boost."""

    type: Literal["BuyRoomBoostResponse"] = Field(alias="_type")
    result: Literal["success", "insufficient_funds", "only_token_bought"]


class TipUserResponse(BaseModel):
    """Tip a user."""

    type: Literal["TipUserResponse"] = Field(alias="_type")
    result: Literal["success", "insufficient_funds"]


class SetOutfitResponse(BaseModel):
    """Set the outfit of a user."""

    type: Literal["SetOutfitResponse"] = Field(alias="_type")


class GetInventoryResponse(BaseModel):
    """Get the inventory of a user."""

    type: Literal["GetInventoryResponse"] = Field(alias="_type")
    items: list[Item]


class BuyItemResponse(BaseModel):
    """Buy an item."""

    type: Literal["BuyItemResponse"] = Field(alias="_type")
    result: Literal["success", "insufficient_funds"]
