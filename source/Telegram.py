import asyncio
from telethon.sync import TelegramClient
from source.FileOperation import FileOperation


class Telegram:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)

    async def list_chats(self):
        await self.__connect()
        dialogs = await self.client.get_dialogs()
        FileOperation.write_chats(self.phone_number, dialogs)

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id, delay, keywords):
        await self.__connect()
        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            # Get new messages since the last checked message
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)
            for message in reversed(messages):
                if keywords:
                    if message.text and any(keyword in message.text.lower() for keyword in keywords):
                        await self.client.send_message(destination_channel_id, message.text)
                        print(f"Message contains a keyword forwarded: {message.text}")
                else:
                    await self.client.send_message(destination_channel_id, message.text)
                    # time = f'{message.date}\n{datetime.now(message.date.tzinfo)}'
                    # await self.client.send_message(destination_channel_id, time)
                    print(f"Message forwarded: {message.text}")

                last_message_id = max(last_message_id, message.id)
            await asyncio.sleep(delay)
    @staticmethod
    def read_config(use_old):
        if use_old:
            api_id, api_hash, phone_number = FileOperation.read_credentials()
        if not use_old or None in (api_id, api_hash, phone_number):
            api_id = input("Enter your API ID: ")
            api_hash = input("Enter your API Hash: ")
            phone_number = input("Enter your phone number: ")
            FileOperation.write_credentials(api_id, api_hash, phone_number)
        return api_id, api_hash, phone_number

    @staticmethod
    def read_forward_config(use_old):
        if use_old:
            source, destination, delay, keywords = FileOperation.read_forward_config()
        if not use_old or None in (source, destination, delay, keywords):
            source = int(input("Enter the source chat ID: "))
            destination = int(input("Enter the destination chat ID: "))
            delay = int(input("Enter delay time between checking chats in seconds: "))
            print("Enter keywords (comma separated) to filter messages or leave blank to forward all: ")
            keywords = input().split(",")
            FileOperation.write_forward_config(source, destination, delay, keywords)
        return source, destination, delay, keywords

    async def __connect(self):
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the login code: '))
