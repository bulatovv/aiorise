from pydantic import BaseModel, Field
from typing import Literal, Any
from aiorise.objects.object_types import *


class ChatRequest(BaseModel):
    """Send a chat message to a room.

    The chat message will be broadcast to everyone in the room, or whispered to `whisper_target_id` if provided.
    """

    type: Literal["ChatRequest"] = Field(alias="_type")
    message: str
    whisper_target_id: str | None = None


class ChannelRequest(BaseModel):
    """Send a hidden channel message to the room.

    This message not be displayed in the chat, so it can be used to
    communicate between bots or client-side scripts."""

    type: Literal["ChannelRequest"] = Field(alias="_type")
    message: str
    tags: list[str] | None = None


class EmoteRequest(BaseModel):
    """Perform an emote.

    Some of the available emotes are:
    * "emoji-angry",
    * "emoji-thumbsup",
    * "emote-hello",
    * "emote-tired",
    * "dance-macarena"

    `target_user_id` can be provided if the emote can be directed toward a player."""

    type: Literal["EmoteRequest"] = Field(alias="_type")
    emote_id: str
    target_user_id: str | None = None


class ReactionRequest(BaseModel):
    """Send a reaction to a user."""

    type: Literal["ReactionRequest"] = Field(alias="_type")
    reaction: Literal["clap", "heart", "thumbs", "wave", "wink"]
    target_user_id: str


class KeepaliveRequest(BaseModel):
    """Send a keepalive request.

    This must be sent every 15 seconds or the server will terminate the connection."""

    type: Literal["KeepaliveRequest"] = Field(alias="_type")


class TeleportRequest(BaseModel):
    """Teleport the provided `user_id` to the provided `destination`."""

    type: Literal["TeleportRequest"] = Field(alias="_type")
    user_id: str


class FloorHitRequest(BaseModel):
    """Move the bot to the given `destination`."""

    type: Literal["FloorHitRequest"] = Field(alias="_type")


class GetRoomUsersRequest(BaseModel):
    """Fetch the list of users currently in the room, with their positions."""

    type: Literal["GetRoomUsersRequest"] = Field(alias="_type")


class GetWalletRequest(BaseModel):
    """Fetch the bot's wallet.

    The wallet contains Highrise currencies."""

    type: Literal["GetWalletRequest"] = Field(alias="_type")


class ModerateRoomRequest(BaseModel):
    """Moderate the room.

    This can be used to kick, ban, unban, or mute a user."""

    type: Literal["ModerateRoomRequest"] = Field(alias="_type")
    user_id: str
    moderation_action: Literal["kick", "ban", "unban", "mute"]
    action_length: int | None = None


class GetRoomPrivilegeRequest(BaseModel):
    """Fetch the room privileges for provided `user_id`."""

    type: Literal["GetRoomPrivilegeRequest"] = Field(alias="_type")
    user_id: str


class ChangeRoomPrivilegeRequest(BaseModel):
    """Change the room privileges for provided `user_id`.
    This can be used to both give and take moderation and designer privileges for current room.

    Bots have to be in the room to change privileges.
    Bots are using their owner's privileges."""

    type: Literal["ChangeRoomPrivilegeRequest"] = Field(alias="_type")
    user_id: str


class MoveUserToRoomRequest(BaseModel):
    """Move the provided `user_id` to the provided `room_id`."""

    type: Literal["MoveUserToRoomRequest"] = Field(alias="_type")
    user_id: str
    room_id: str


class AnchorHitRequest(BaseModel):
    """Move the bot to the given furniture Anchor Position."""

    type: Literal["AnchorHitRequest"] = Field(alias="_type")


class InviteSpeakerRequest(BaseModel):
    """Invite a user to speak in the room."""

    type: Literal["InviteSpeakerRequest"] = Field(alias="_type")
    user_id: str


class RemoveSpeakerRequest(BaseModel):
    """Remove a user from speaking in the room."""

    type: Literal["RemoveSpeakerRequest"] = Field(alias="_type")
    user_id: str


class CheckVoiceChatRequest(BaseModel):
    """Check the voice chat status in the room."""

    type: Literal["CheckVoiceChatRequest"] = Field(alias="_type")


class GetUserOutfitRequest(BaseModel):
    """Get the outfit of a user."""

    type: Literal["GetUserOutfitRequest"] = Field(alias="_type")
    user_id: str


class GetBackpackRequest(BaseModel):
    """Fetch a user's world backpack."""

    type: Literal["GetBackpackRequest"] = Field(alias="_type")
    user_id: str


class GetMessagesRequest(BaseModel):
    """Get the messages of a conversation. 20 messages will be returned at most, if all 20 messages are returned, the
    last_message_id can be used to retrieve the next 20 messages. conversation_id must be provided.
    """

    type: Literal["GetMessagesRequest"] = Field(alias="_type")
    conversation_id: str
    last_message_id: str | None = None


class SendMessageRequest(BaseModel):
    """Send a message to a conversation. If bot wishes to send room invite, the room_id must be provided."""

    type: Literal["SendMessageRequest"] = Field(alias="_type")
    conversation_id: str
    content: str
    type: Literal["text", "invite"]
    room_id: str | None = None


class GetConversationsRequest(BaseModel):
    """Get the conversations of a bat. if not_joined is true, only get the conversations that bot has not joined yet will
    be returned. 20 conversations will be returned at most, if all 20 conversations are returned, the last_id can be used
    to retrieve the next 20 conversations."""

    type: Literal["GetConversationsRequest"] = Field(alias="_type")
    not_joined: bool | None = None
    last_id: str | None = None


class LeaveConversationRequest(BaseModel):
    """Leave a conversation."""

    type: Literal["LeaveConversationRequest"] = Field(alias="_type")
    conversation_id: str


class BuyVoiceTimeRequest(BaseModel):
    """Buy a voice time for a room."""

    type: Literal["BuyVoiceTimeRequest"] = Field(alias="_type")
    payment_method: Literal[
        "bot_wallet_only", "bot_wallet_priority", "user_wallet_only"
    ]


class BuyRoomBoostRequest(BaseModel):
    """Buy a room boost."""

    type: Literal["BuyRoomBoostRequest"] = Field(alias="_type")
    payment_method: Literal[
        "bot_wallet_only", "bot_wallet_priority", "user_wallet_only"
    ]
    amount: int | None = None


class TipUserRequest(BaseModel):
    """Tip a user."""

    type: Literal["TipUserRequest"] = Field(alias="_type")
    user_id: str
    gold_bar: Literal[
        "gold_bar_1",
        "gold_bar_5",
        "gold_bar_10",
        "gold_bar_50",
        "gold_bar_100",
        "gold_bar_500",
        "gold_bar_1k",
        "gold_bar_5000",
        "gold_bar_10k",
    ]


class SetOutfitRequest(BaseModel):
    """Set the outfit of a user."""

    type: Literal["SetOutfitRequest"] = Field(alias="_type")
    outfit: list[Item]


class GetInventoryRequest(BaseModel):
    """Get the inventory of a user."""

    type: Literal["GetInventoryRequest"] = Field(alias="_type")


class BuyItemRequest(BaseModel):
    """Buy an item."""

    type: Literal["BuyItemRequest"] = Field(alias="_type")
    item_id: str
