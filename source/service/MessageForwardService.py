import os
from typing import Optional, List

from telethon import TelegramClient
from telethon.tl.custom import Message

from source.utils.Constants import MEDIA_FOLDER_PATH


class MessageForwardService:
    """Service for handling message forwarding and sending operations."""

    def __init__(self, client: TelegramClient):
        """Initialize the message forward service.
        
        Args:
            client: Telegram client instance
        """
        self.client = client

    async def forward_message(self, destination_id: int, message: Message, reply_to: Optional[int] = None) -> Optional[Message]:
        try:
            if message.forward is not None:
                return await self.client.forward_messages(destination_id, message)

            media_path = None
            try:
                if message.media:
                    media_path = await self._download_media(message)
                
                text = message.text or ''
                
                if media_path:
                    return await self.client.send_file(
                        destination_id,
                        media_path,
                        caption=text,
                        reply_to=reply_to
                    )
                else:
                    return await self.client.send_message(
                        destination_id,
                        text,
                        reply_to=reply_to
                    )
            finally:
                if media_path:
                    self._delete_media(media_path)

        except Exception as e:
            print(f"Error sending message: {e}")
            return None

    async def forward_album(
        self,
        destination_id: int,
        messages: List[Message],
        caption: str,
        reply_to: Optional[int] = None
    ) -> Optional[List[Message]]:
        media_paths = []
        try:
            media_paths = await self._download_album_media(messages)
            return await self.client.send_file(
                destination_id,
                media_paths,
                caption=caption,
                reply_to=reply_to
            )
        except Exception as e:
            print(f"Error forwarding album: {e}")
            return None
        finally:
            self._cleanup_media(media_paths)

    async def _download_media(self, message: Message) -> Optional[str]:
        try:
            os.makedirs(MEDIA_FOLDER_PATH, exist_ok=True)
            return await self.client.download_media(message, file=MEDIA_FOLDER_PATH)
        except Exception as e:
            print(f"Error downloading media: {e}")
            return None

    async def _download_album_media(self, messages: List[Message]) -> List[str]:
        media_paths = []
        for message in messages:
            if message.media:
                path = await self._download_media(message)
                if path:
                    media_paths.append(path)
        return media_paths

    @staticmethod
    def _delete_media(media_path: str) -> None:
        try:
            os.remove(media_path)
        except Exception as e:
            print(f"Error deleting media file {media_path}: {e}")

    @staticmethod
    def _cleanup_media(media_paths: List[str]) -> None:
        for path in media_paths:
            MessageForwardService._delete_media(path) 