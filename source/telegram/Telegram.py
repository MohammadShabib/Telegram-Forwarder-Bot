import os
import json

import telethon
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty

from source.model.Chat import Chat
from source.telegram.Forward import Forward
from source.utils.Constants import SESSION_PREFIX_PATH, MEDIA_FOLDER_PATH, IGNORE_CHATS_FILE_PATH


class Telegram:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = TelegramClient(SESSION_PREFIX_PATH + credentials.phone_number, credentials.api_id,
                                     credentials.api_hash)

    async def list_chats(self):
        await self.__connect()
        chats = await self.client.get_dialogs()
        Chat.write(chats)

    async def delete(self, ignore_chats):
        await self.__connect()

        # Get my user ID from client
        me = await self.client.get_me()
        my_username = me.id

        ignored_ids = [chat.id for chat in ignore_chats]
        
        async for dialog in self.client.iter_dialogs():
            try:
                if not dialog.is_group:
                    continue
                chat = dialog.entity
                if (dialog.id == my_username or dialog.id in ignored_ids):
                    continue
                
                print(f"Searching in chat: {chat.username if chat.username else chat.title}")

                # Search messages in the current chat
                async for message in self.client.iter_messages(chat, from_user=my_username):
                    print(f"Chat: {chat.username if chat.username else chat.title}")
                    await self.client.delete_messages(chat, message.id)

            except Exception as e:
                print(e)

    async def findUser(self, wanted_user):
        await self.__connect()

        # Get my user ID from client
        me = await self.client.get_me()
        my_id = me.id
        
        async for dialog in self.client.iter_dialogs():
            chat = dialog.entity
            try:
                if chat.id == my_id and wanted_user.id != my_id:
                    continue

                async for message in self.client.iter_messages(chat, from_user=wanted_user.id):
                    if isinstance(chat, telethon.tl.types.User):
                        break

                    print(f"Chat: {chat.title}")
                    print(message.date)
                    print(message.text)
                    print(f"https://t.me/c/{message.peer_id.channel_id}/{message.id}")
                    await self.download_media(message)

            except Exception as e:
                print(e)

    async def download_media(self, message):
        if not os.path.exists(MEDIA_FOLDER_PATH):
            os.makedirs(MEDIA_FOLDER_PATH)

        file_path = await self.client.download_media(message, file=MEDIA_FOLDER_PATH)
        return file_path

    async def start_forward(self, forward_config):
        await self.__connect()
        forward = Forward(self.client, forward_config)
        forward.add_events()
        await self.client.run_until_disconnected()

    async def past(self, forward_config):
        await self.__connect()
        forward = Forward(self.client, forward_config)
        await forward.forward_all_history()

    async def __connect(self):
        await self.client.connect()
        await self.client.start(self.credentials.phone_number)
