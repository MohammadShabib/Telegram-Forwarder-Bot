import asyncio
import os
import logging
from telethon.sync import TelegramClient
from source.model.Chat import Chat

class Telegram:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = TelegramClient('sessions/session_' + credentials.phone_number, credentials.api_id, credentials.api_hash)

    async def list_chats(self):
        await self.__connect()
        chats = await self.client.get_dialogs()
        Chat.write(chats)

    async def start_forward(self, forwardConfig):
        await self.__connect()
        last_message_id = (await self.client.get_messages(forwardConfig.sourceID, limit=1))[0].id
        while True:
            messages = await self.client.get_messages(forwardConfig.sourceID, min_id=last_message_id, limit=None)
            for message in reversed(messages):
                print(
                    f"Message will be sent: {message.text}. From: {forwardConfig.sourceName}. To: {forwardConfig.destinationName}.")
                await self.forward_message(forwardConfig.destinationID, message)
                last_message_id = max(last_message_id, message.id)
            await asyncio.sleep(forwardConfig.delay)

    async def forward_message(self, destination_channel_id, message):
        media_path = None
        if message.media:
            media_path = await self.download_media(message)
        text = message.text if message.text else ''
        if media_path:
            await self.client.send_file(destination_channel_id, media_path, caption=text)
            self.delete_media(media_path)
        else:
            await self.client.send_message(destination_channel_id, text)

        # time = f'{message.date}\n{datetime.now(message.date.tzinfo)}'
        # await self.client.send_message(destination_channel_id, time)

    async def __connect(self):
        await self.client.connect()
        await self.client.start(self.credentials.phone_number)

    async def download_media(self, message):
        download_folder = 'media'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        file_path = await self.client.download_media(message, file=download_folder)
        return file_path

    def delete_media(self, media_path):
        os.remove(media_path)
