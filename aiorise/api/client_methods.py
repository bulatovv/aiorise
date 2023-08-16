from aiorise.api.response_types import *
from aiorise.api.protocols import HaveApiConnection


class HighriseWebApiMethods:
    async def chat(
        self: HaveApiConnection, message: str, whisper_target_id: str | None = None
    ) -> None:
        """Send a chat message to a room.

        The chat message will be broadcast to everyone in the room, or whispered to `whisper_target_id` if provided.
        """
        await self._connection.send(
            {
                "_type": "ChatRequest",
                "message": message,
                "whisper_target_id": whisper_target_id,
            },
            False,
        )

    async def channel(
        self: HaveApiConnection, message: str, tags: list[str] | None = None
    ) -> ChannelResponse:
        """Send a hidden channel message to the room.

        This message not be displayed in the chat, so it can be used to
        communicate between bots or client-side scripts."""
        return ChannelResponse.model_validate(
            await self._connection.send(
                {"_type": "ChannelRequest", "message": message, "tags": tags}
            )
        )

    async def emote(
        self: HaveApiConnection, emote_id: str, target_user_id: str | None = None
    ) -> EmoteResponse:
        """Perform an emote.

        Some of the available emotes are:
        * "emoji-angry",
        * "emoji-thumbsup",
        * "emote-hello",
        * "emote-tired",
        * "dance-macarena"

        `target_user_id` can be provided if the emote can be directed toward a player.
        """
        return EmoteResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "EmoteRequest",
                    "emote_id": emote_id,
                    "target_user_id": target_user_id,
                }
            )
        )

    async def reaction(
        self: HaveApiConnection,
        reaction: Literal["clap", "heart", "thumbs", "wave", "wink"],
        target_user_id: str,
    ) -> ReactionResponse:
        """Send a reaction to a user."""
        return ReactionResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "ReactionRequest",
                    "reaction": reaction,
                    "target_user_id": target_user_id,
                }
            )
        )

    async def keepalive(self: HaveApiConnection) -> KeepaliveResponse:
        """Send a keepalive request.

        This must be sent every 15 seconds or the server will terminate the connection.
        """
        return KeepaliveResponse.model_validate(
            await self._connection.send({"_type": "KeepaliveRequest"})
        )

    async def teleport(self: HaveApiConnection, user_id: str) -> TeleportResponse:
        """Teleport the provided `user_id` to the provided `destination`."""
        return TeleportResponse.model_validate(
            await self._connection.send(
                {"_type": "TeleportRequest", "user_id": user_id}
            )
        )

    async def floor_hit(self: HaveApiConnection) -> FloorHitResponse:
        """Move the bot to the given `destination`."""
        return FloorHitResponse.model_validate(
            await self._connection.send({"_type": "FloorHitRequest"})
        )

    async def get_room_users(self: HaveApiConnection) -> GetRoomUsersResponse:
        """Fetch the list of users currently in the room, with their positions."""
        return GetRoomUsersResponse.model_validate(
            await self._connection.send({"_type": "GetRoomUsersRequest"})
        )

    async def get_wallet(self: HaveApiConnection) -> GetWalletResponse:
        """Fetch the bot's wallet.

        The wallet contains Highrise currencies."""
        return GetWalletResponse.model_validate(
            await self._connection.send({"_type": "GetWalletRequest"})
        )

    async def moderate_room(
        self: HaveApiConnection,
        user_id: str,
        moderation_action: Literal["kick", "ban", "unban", "mute"],
        action_length: int | None = None,
    ) -> ModerateRoomResponse:
        """Moderate the room.

        This can be used to kick, ban, unban, or mute a user."""
        return ModerateRoomResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "ModerateRoomRequest",
                    "user_id": user_id,
                    "moderation_action": moderation_action,
                    "action_length": action_length,
                }
            )
        )

    async def get_room_privilege(
        self: HaveApiConnection, user_id: str
    ) -> GetRoomPrivilegeResponse:
        """Fetch the room privileges for provided `user_id`."""
        return GetRoomPrivilegeResponse.model_validate(
            await self._connection.send(
                {"_type": "GetRoomPrivilegeRequest", "user_id": user_id}
            )
        )

    async def change_room_privilege(
        self: HaveApiConnection, user_id: str
    ) -> ChangeRoomPrivilegeResponse:
        """Change the room privileges for provided `user_id`.
        This can be used to both give and take moderation and designer privileges for current room.

        Bots have to be in the room to change privileges.
        Bots are using their owner's privileges."""
        return ChangeRoomPrivilegeResponse.model_validate(
            await self._connection.send(
                {"_type": "ChangeRoomPrivilegeRequest", "user_id": user_id}
            )
        )

    async def move_user_to_room(
        self: HaveApiConnection, user_id: str, room_id: str
    ) -> MoveUserToRoomResponse:
        """Move the provided `user_id` to the provided `room_id`."""
        return MoveUserToRoomResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "MoveUserToRoomRequest",
                    "user_id": user_id,
                    "room_id": room_id,
                }
            )
        )

    async def anchor_hit(self: HaveApiConnection) -> AnchorHitResponse:
        """Move the bot to the given furniture Anchor Position."""
        return AnchorHitResponse.model_validate(
            await self._connection.send({"_type": "AnchorHitRequest"})
        )

    async def invite_speaker(self: HaveApiConnection, user_id: str) -> None:
        """Invite a user to speak in the room."""
        await self._connection.send(
            {"_type": "InviteSpeakerRequest", "user_id": user_id}, False
        )

    async def remove_speaker(self: HaveApiConnection, user_id: str) -> None:
        """Remove a user from speaking in the room."""
        await self._connection.send(
            {"_type": "RemoveSpeakerRequest", "user_id": user_id}, False
        )

    async def check_voice_chat(self: HaveApiConnection) -> CheckVoiceChatResponse:
        """Check the voice chat status in the room."""
        return CheckVoiceChatResponse.model_validate(
            await self._connection.send({"_type": "CheckVoiceChatRequest"})
        )

    async def get_user_outfit(
        self: HaveApiConnection, user_id: str
    ) -> GetUserOutfitResponse:
        """Get the outfit of a user."""
        return GetUserOutfitResponse.model_validate(
            await self._connection.send(
                {"_type": "GetUserOutfitRequest", "user_id": user_id}
            )
        )

    async def get_backpack(self: HaveApiConnection, user_id: str) -> None:
        """Fetch a user's world backpack."""
        await self._connection.send(
            {"_type": "GetBackpackRequest", "user_id": user_id}, False
        )

    async def get_messages(
        self: HaveApiConnection,
        conversation_id: str,
        last_message_id: str | None = None,
    ) -> GetMessagesResponse:
        """Get the messages of a conversation. 20 messages will be returned at most, if all 20 messages are returned, the
        last_message_id can be used to retrieve the next 20 messages. conversation_id must be provided.
        """
        return GetMessagesResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "GetMessagesRequest",
                    "conversation_id": conversation_id,
                    "last_message_id": last_message_id,
                }
            )
        )

    async def send_message(
        self: HaveApiConnection,
        conversation_id: str,
        content: str,
        type: Literal["text", "invite"],
        room_id: str | None = None,
    ) -> SendMessageResponse:
        """Send a message to a conversation. If bot wishes to send room invite, the room_id must be provided."""
        return SendMessageResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "SendMessageRequest",
                    "conversation_id": conversation_id,
                    "content": content,
                    "type": type,
                    "room_id": room_id,
                }
            )
        )

    async def get_conversations(
        self: HaveApiConnection,
        not_joined: bool | None = None,
        last_id: str | None = None,
    ) -> GetConversationsResponse:
        """Get the conversations of a bat. if not_joined is true, only get the conversations that bot has not joined yet will
        be returned. 20 conversations will be returned at most, if all 20 conversations are returned, the last_id can be used
        to retrieve the next 20 conversations."""
        return GetConversationsResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "GetConversationsRequest",
                    "not_joined": not_joined,
                    "last_id": last_id,
                }
            )
        )

    async def leave_conversation(
        self: HaveApiConnection, conversation_id: str
    ) -> LeaveConversationResponse:
        """Leave a conversation."""
        return LeaveConversationResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "LeaveConversationRequest",
                    "conversation_id": conversation_id,
                }
            )
        )

    async def buy_voice_time(
        self: HaveApiConnection,
        payment_method: Literal[
            "bot_wallet_only", "bot_wallet_priority", "user_wallet_only"
        ],
    ) -> BuyVoiceTimeResponse:
        """Buy a voice time for a room."""
        return BuyVoiceTimeResponse.model_validate(
            await self._connection.send(
                {"_type": "BuyVoiceTimeRequest", "payment_method": payment_method}
            )
        )

    async def buy_room_boost(
        self: HaveApiConnection,
        payment_method: Literal[
            "bot_wallet_only", "bot_wallet_priority", "user_wallet_only"
        ],
        amount: int | None = None,
    ) -> BuyRoomBoostResponse:
        """Buy a room boost."""
        return BuyRoomBoostResponse.model_validate(
            await self._connection.send(
                {
                    "_type": "BuyRoomBoostRequest",
                    "payment_method": payment_method,
                    "amount": amount,
                }
            )
        )

    async def tip_user(
        self: HaveApiConnection,
        user_id: str,
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
        ],
    ) -> TipUserResponse:
        """Tip a user."""
        return TipUserResponse.model_validate(
            await self._connection.send(
                {"_type": "TipUserRequest", "user_id": user_id, "gold_bar": gold_bar}
            )
        )

    async def set_outfit(
        self: HaveApiConnection, outfit: list[Item]
    ) -> SetOutfitResponse:
        """Set the outfit of a user."""
        return SetOutfitResponse.model_validate(
            await self._connection.send({"_type": "SetOutfitRequest", "outfit": outfit})
        )

    async def get_inventory(self: HaveApiConnection) -> GetInventoryResponse:
        """Get the inventory of a user."""
        return GetInventoryResponse.model_validate(
            await self._connection.send({"_type": "GetInventoryRequest"})
        )

    async def buy_item(self: HaveApiConnection, item_id: str) -> BuyItemResponse:
        """Buy an item."""
        return BuyItemResponse.model_validate(
            await self._connection.send({"_type": "BuyItemRequest", "item_id": item_id})
        )
