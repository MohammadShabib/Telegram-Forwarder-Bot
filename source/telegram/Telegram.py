import asyncio
import os
import logging
from telethon.sync import TelegramClient
from source.model.Chat import Chat
from source.telegram.Forward import Forward
from source.utils.Constants import SESSION_PREFIX_PATH


class Telegram:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = TelegramClient(SESSION_PREFIX_PATH + credentials.phone_number, credentials.api_id,
                                     credentials.api_hash)

    async def list_chats(self):
        await self.__connect()
        chats = await self.client.get_dialogs()
        Chat.write(chats)

    async def start_forward(self, forwardConfig):
        await self.__connect()
        Forward(self.client, forwardConfig)
        await self.client.run_until_disconnected()

    async def __connect(self):
        await self.client.connect()
        await self.client.start(self.credentials.phone_number)
