import json
import os

from source.utils.Constants import CHAT_FILE_PATH, IGNORE_CHATS_FILE_PATH, WANTED_USER_FILE_PATH
from source.utils.Utilities import Utilities


class Chat:

    def __init__(self, id=None, title=None, type=None, username=None):
        self.id = id
        self.title = title
        self.type = type
        self.username = username

    @staticmethod
    def write(chats):
        chats_list = []
        username = None
        for chat in chats:
            chat_type = "UNKNOWN"
            if chat.is_channel:
                chat_type = "Channel"
            elif chat.is_group:
                chat_type = "Group"
            elif chat.is_user:
                chat_type = "User"
                username = chat.entity.username

            chat_dict = {
                "id": chat.id,
                "title": chat.title,
                "type": chat_type,
                "username": username
            }
            print(f"Chat ID: {chat.id}, Title: {chat.title}, Type: {chat_type}")
            chats_list.append(chat_dict)

        with open(CHAT_FILE_PATH, "w") as chats_file:
            json.dump(chats_list, chats_file, indent=4)

    @staticmethod
    def read():
        with open(CHAT_FILE_PATH, "r") as chats_file:
            chats_list = json.load(chats_file)
        return [Chat(**chat) for chat in chats_list]

    @staticmethod
    def read_ignore_chats():
        with open(IGNORE_CHATS_FILE_PATH, "r") as chats_file:
            chats_list = json.load(chats_file)
        return [Chat(**chat) for chat in chats_list]

    @staticmethod
    def read_wanted_user():
        with open(WANTED_USER_FILE_PATH, "r") as user_file:
            user_data = json.load(user_file)
        return Chat(**user_data)

    @staticmethod
    def write_ignore_chats(chats_list):
        with open(IGNORE_CHATS_FILE_PATH, "w") as chats_file:
            json.dump([chat.__dict__ for chat in chats_list], chats_file, indent=4)

    @staticmethod
    def write_wanted_user(chat):
        with open(WANTED_USER_FILE_PATH, "w") as user_file:
            json.dump(chat.__dict__, user_file, indent=4)

    @staticmethod
    async def scan_ignore_chats():
        chats = Chat.read()
        ignore_list = []
        while True:
            choice = await Utilities.list_chats_terminal(chats, "ignore")
            if choice == -1:
                break
            ignore_list.append(chats[choice])
        Chat.write_ignore_chats(ignore_list)
        return ignore_list

    @staticmethod
    async def scan_wanted_user():
        chats = Chat.read()
        choice = await Utilities.list_chats_terminal(chats, "target")
        if choice == -1:
            return None
        wanted_user = chats[choice]
        Chat.write_wanted_user(wanted_user)
        return wanted_user

    @staticmethod
    async def get_ignore_chats(is_saved=True):
        if is_saved and os.path.exists(IGNORE_CHATS_FILE_PATH):
            return Chat.read_ignore_chats()
        else:
            return await Chat.scan_ignore_chats()

    @staticmethod
    async def get_wanted_user(is_saved=True):
        if is_saved and os.path.exists(WANTED_USER_FILE_PATH):
            return Chat.read_wanted_user()
        else:
            return await Chat.scan_wanted_user()
