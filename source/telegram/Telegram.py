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
