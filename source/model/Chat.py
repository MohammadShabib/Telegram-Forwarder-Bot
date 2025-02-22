import json
import os

from source.utils.Constants import CHAT_FILE_PATH, IGNORE_CHATS_FILE_PATH, WANTED_USER_FILE_PATH
from source.dialog.BaseDialog import BaseDialog


class Chat:
    """A class representing a Telegram chat entity with persistence capabilities.
    
    This class handles chat data management including reading/writing chat information
    to files and managing ignore lists and wanted user configurations.
    
    Attributes:
        id (int): The Telegram chat ID
        title (str): The chat title/name
        type (str): The type of chat (Channel, Group, User, or UNKNOWN)
        username (str): The username associated with the chat
    """

    def __init__(self, id: int = None, title: str = None, type: str = None, username: str = None):
        self.id = id
        self.title = title
        self.type = type
        self.username = username

    @staticmethod
    def write(chats) -> list:
        """Writes chat information to a file.
        
        Args:
            chats: List of Telegram chat objects to persist
            
        Returns:
            list: List of processed chat dictionaries
        """
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
            chats_list.append(chat_dict)

        with open(CHAT_FILE_PATH, "w") as chats_file:
            json.dump(chats_list, chats_file, indent=4)
        return chats_list

    @staticmethod
    def read() -> list['Chat']:
        """Reads chat information from file.
        
        Returns:
            list[Chat]: List of Chat objects loaded from file
        """
        with open(CHAT_FILE_PATH, "r") as chats_file:
            chats_list = json.load(chats_file)
        return [Chat(**chat) for chat in chats_list]

    @staticmethod
    def read_ignore_chats():
        with open(IGNORE_CHATS_FILE_PATH, "r") as chats_file:
            chats_list = json.load(chats_file)
        return [Chat(**chat) for chat in chats_list]

    @staticmethod
    def read_wanted_users():
        """Reads wanted users from file.
        
        Returns:
            list[Chat]: List of Chat objects for wanted users
        """
        with open(WANTED_USER_FILE_PATH, "r") as user_file:
            users_data = json.load(user_file)
            # Handle both single user (dict) and multiple users (list) formats
            if isinstance(users_data, dict):
                return [Chat(**users_data)]
            return [Chat(**user) for user in users_data]

    @staticmethod
    def write_ignore_chats(chats_list):
        with open(IGNORE_CHATS_FILE_PATH, "w") as chats_file:
            json.dump([chat.__dict__ for chat in chats_list], chats_file, indent=4)

    @staticmethod
    def write_wanted_users(chats_list):
        """Writes wanted users to file.
        
        Args:
            chats_list: List of Chat objects to save
        """
        with open(WANTED_USER_FILE_PATH, "w") as user_file:
            json.dump([chat.__dict__ for chat in chats_list], user_file, indent=4)

    @staticmethod
    async def scan_ignore_chats() -> list['Chat']:
        """Interactively scans for chats to ignore.
        
        Returns:
            list[Chat]: List of Chat objects to ignore
        """
        chats = Chat.read()
        ignore_list = []
        dialog = BaseDialog()
        
        while True:
            choice = await dialog.list_chats_terminal(chats, "ignore")
            if choice == -1:
                break
            ignore_list.append(chats[choice])
        Chat.write_ignore_chats(ignore_list)
        return ignore_list

    @staticmethod
    async def scan_wanted_user() -> 'Chat':
        """Interactively scans for a wanted user.
        
        Returns:
            Chat: The selected wanted user Chat object, or None if cancelled
        """
        chats = Chat.read()
        dialog = BaseDialog()
        choice = await dialog.list_chats_terminal(chats, "target")
        if choice == -1:
            return None
        wanted_user = chats[choice]
        Chat.write_wanted_users([wanted_user])
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
            return Chat.read_wanted_users()[0]
        else:
            return await Chat.scan_wanted_user()

    def get_display_name(self) -> str:
        """Returns a standardized display string for the chat with Rich formatting.
        
        Returns:
            str: Formatted string with chat information including type, ID, username and title
        """
        type_color = {
            "Channel": "cyan",
            "Group": "green",
            "User": "yellow",
            "UNKNOWN": "red"
        }.get(self.type, "white")

        # Pad all fields to fixed widths
        type_padded = f"Type: {self.type:<10}"
        id_padded = f"ID: {self.id:<15}"
        username_padded = f"Username: {self.username if self.username else '':<30}"
        title_padded = f"Title: {self.title:<100}"
        
        display_parts = [
            f"[{type_color}]{type_padded}[/]",
            f"[dim]{id_padded}[/]",
            f"[blue]{username_padded}[/]",
            f"[bold]{title_padded}[/]"
        ]
        return " | ".join(display_parts)

    def get_plain_display_name(self):
        """Returns a plain text version without Rich formatting"""
        # Pad all fields to fixed widths
        type_padded = f"Type: {self.type:<10}"
        id_padded = f"ID: {self.id:<15}"
        username_padded = f"Username: {self.username if self.username else '':<30}"
        title_padded = f"Title: {self.title:<100}"
        
        display_parts = [
            type_padded,
            id_padded,
            username_padded,
            title_padded
        ]
        return " | ".join(display_parts)
