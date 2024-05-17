import json

from source.utils.Constants import CHAT_FILE_PATH


class Chat:

    def __init__(self, id=None, title=None, type=None):
        self.id = id
        self.title = title
        self.type = type

    @staticmethod
    def write(chats):
        chats_list = []
        for chat in chats:
            chat_type = "UNKNOWN"
            if chat.is_channel:
                chat_type = "Channel"
            elif chat.is_group:
                chat_type = "Group"
            elif chat.is_user:
                chat_type = "User"

            chat_dict = {
                "id": chat.id,
                "title": chat.title,
                "type": chat_type
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
