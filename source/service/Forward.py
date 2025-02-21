from typing import Optional, List

from telethon import events, TelegramClient
from telethon.tl.custom import Message

from source.service.HistoryService import HistoryService
from source.service.MessageForwardService import MessageForwardService


class Forward:
    """Service class for handling message forwarding operations.
    
    This class manages both live message forwarding and historical message forwarding
    between configured source and destination chats.
    
    Attributes:
        client (TelegramClient): The Telegram client instance
        forward_config_map (dict): Mapping of source chat IDs to forward configurations
        history (HistoryService): Service for tracking message forwarding history
        message_forward (MessageForwardService): Service for handling message forwarding operations
    """

    def __init__(self, client: TelegramClient, forward_config_map: dict):
        """Initialize Forward service.
        
        Args:
            client: Telegram client instance
            forward_config_map: Mapping of source chat IDs to forward configurations
        """
        self.client = client
        self.forward_config_map = forward_config_map
        self.history = HistoryService()
        self.message_forward = MessageForwardService(client)

    def add_events(self) -> None:
        """Register message and album event handlers."""
        source_chats = list(self.forward_config_map.keys())
        self.client.add_event_handler(
            self.message_handler,
            events.NewMessage(chats=source_chats)
        )
        self.client.add_event_handler(
            self.album_handler,
            events.Album(chats=source_chats)
        )

    async def message_handler(self, event: events.NewMessage.Event) -> None:
        """Handle single message events.
        
        Args:
            event: New message event
        """
        try:
            if event.grouped_id:
                return

            destination_id = self._get_destination_id(event.chat_id)
            if not destination_id:
                return

            reply_message = await self._handle_reply(event.message, destination_id)
            await self._forward_message(destination_id, event.message, reply_message)

        except Exception as e:
            print(f"Error handling message: {e}")

    async def album_handler(self, event: events.Album.Event) -> None:
        """Handle album/media group events.
        
        Args:
            event: Album event
        """
        try:
            destination_id = self._get_destination_id(event.chat_id)
            if not destination_id:
                return

            reply_message = await self._get_album_reply(event.messages, destination_id)
            await self._forward_album(destination_id, event, reply_message)

        except Exception as e:
            print(f"Error handling album: {e}")

    async def history_handler(self) -> None:
        """Forward all historical messages from source chats."""
        last_message_id = 0
        for source in self.forward_config_map:
            await self._forward_chat_history(source, last_message_id)

    async def _forward_chat_history(self, source: int, last_message_id: int) -> None:
        """Forward history from a specific chat.
        
        Args:
            source: Source chat ID
            last_message_id: ID of last processed message
        """
        messages = await self.client.get_messages(source, min_id=last_message_id, limit=None)
        destination_id = self._get_destination_id(source)

        for message in reversed(messages):
            try:
                reply_message = await self._handle_reply(message, destination_id)
                await self._forward_message(destination_id, message, reply_message)
                last_message_id = max(last_message_id, message.id)
            except Exception as e:
                print(f"Error forwarding message: {e}")

    def _get_destination_id(self, source_id: int) -> Optional[int]:
        """Get destination chat ID for a source chat.
        
        Args:
            source_id: Source chat ID
            
        Returns:
            Destination chat ID if found, None otherwise
        """
        config = self.forward_config_map.get(source_id)
        return config.destinationID if config else None

    async def _handle_reply(self, message: Message, destination_id: int) -> Optional[int]:
        """Handle reply-to messages.
        
        Args:
            message: Message object
            destination_id: Destination chat ID
            
        Returns:
            ID of reply message in destination chat if exists
        """
        if not message.is_reply:
            return None
        return self.history.get_mapping(
            message.chat_id,
            message.reply_to_msg_id,
            destination_id
        )

    async def _get_album_reply(self, messages: List[Message], destination_id: int) -> Optional[int]:
        """Get reply message ID for an album.
        
        Args:
            messages: List of messages in album
            destination_id: Destination chat ID
            
        Returns:
            First valid reply message ID found
        """
        for message in messages:
            reply = await self._handle_reply(message, destination_id)
            if reply is not None:
                return reply
        return None

    async def _forward_message(self, destination_id: int, message: Message, reply_to: Optional[int] = None) -> None:
        """Forward a single message.
        
        Args:
            destination_id: Destination chat ID
            message: Message to forward
            reply_to: Optional ID of message to reply to
        """
        try:
            sent_message = await self.message_forward.forward_message(destination_id, message, reply_to)
            if sent_message:
                self._update_history(message, sent_message)
        except Exception as e:
            print(f"Error forwarding message: {e}")

    async def _forward_album(self, destination_id: int, event: events.Album.Event,
                             reply_to: Optional[int] = None) -> None:
        """Forward an album/media group.
        
        Args:
            destination_id: Destination chat ID
            event: Album event
            reply_to: Optional ID of message to reply to
        """
        try:
            sent_messages = await self.message_forward.forward_album(
                destination_id,
                event.messages,
                event.text,
                reply_to
            )
            if sent_messages:
                self._update_album_history(event, sent_messages, destination_id)
        except Exception as e:
            print(f"Error forwarding album: {e}")

    def _update_history(self, source_message: Message, sent_message: Message) -> None:
        """Update message history mapping.
        
        Args:
            source_message: Original message
            sent_message: Forwarded message
        """
        self.history.add_mapping(
            source_message.chat_id,
            source_message.id,
            sent_message.chat_id,
            sent_message.id
        )

    def _update_album_history(self, event: events.Album.Event, sent_messages: List[Message],
                              destination_id: int) -> None:
        """Update history mapping for album messages.
        
        Args:
            event: Album event
            sent_messages: List of sent messages
            destination_id: Destination chat ID
        """
        for i, message in enumerate(event.messages):
            self.history.add_mapping(
                event.chat_id,
                message.id,
                destination_id,
                sent_messages[i].id
            )
