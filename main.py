import asyncio
import os
from source.Telegram import Telegram

async def main():
    api_id, api_hash, phone_number = Telegram.read_config(True)
    telegram = Telegram(api_id, api_hash, phone_number)
    while True:
        print("******************")
        print("Choose an option:")
        print("0. Exist")
        print("1. Update Config")
        print("2. List Chats")
        print("3. Forward Messages")
        choice = input("Enter your choice: ")
        if choice == "0":
            exit()
        if choice == "1":
            os.system("cls")
            telegram.client.disconnect()
            api_id, api_hash, phone_number = Telegram.read_config(True)
            telegram = Telegram(api_id, api_hash, phone_number)
        elif choice == "2":
            os.system("cls")
            await telegram.list_chats()
        elif choice == "3":
            print("1. Use old forward configuration.")
            print("2. new update configuration")
            choice = input("Enter your choice: ")
            use_old = True
            if (choice == "2"):
                use_old = False
            source_chat_id, destination_channel_id, delay, keywords = telegram.read_forward_config(use_old)
            await telegram.forward_messages_to_channel(source_chat_id, destination_channel_id, delay, keywords)
        else:
            print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
