import asyncio
from telethon.sync import TelegramClient

from source.model.Chat import Chat


class Telegram:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = TelegramClient('session_' + credentials.phone_number, credentials.api_id, credentials.api_hash)

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
                await self.forward_message(forwardConfig.destinationID, message)
                print(f"Message forwarded: {message.text}. From: {forwardConfig.sourceName}. To: {forwardConfig.destinationName}.")
                last_message_id = max(last_message_id, message.id)
            await asyncio.sleep(forwardConfig.delay)

    async def forward_message(self, destination_channel_id, message):
        await self.client.send_message(destination_channel_id, message)
        # time = f'{message.date}\n{datetime.now(message.date.tzinfo)}'
        # await self.client.send_message(destination_channel_id, time)

    async def __connect(self):
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.credentials.phone_number)
            await self.client.sign_in(self.credentials.phone_number, input('Enter the login code: '))
