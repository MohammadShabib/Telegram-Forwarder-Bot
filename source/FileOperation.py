import os


class FileOperation:
    os.makedirs("resources")
    credentials_file_path = "resources/credentials.txt"
    chats_file_path = "resources/chats.txt"
    forward_config_file_path = "resources/forwardConfig.txt"
    @staticmethod
    def read_credentials():
        try:
            with open(FileOperation.credentials_file_path, "r") as file:
                lines = file.readlines()
                api_id = lines[0].strip()
                api_hash = lines[1].strip()
                phone_number = lines[2].strip()
                return api_id, api_hash, phone_number
        except FileNotFoundError:
            print("Credentials file not found.")
            return None, None, None

    @staticmethod
    def write_credentials(api_id, api_hash, phone_number):
        with open(FileOperation.credentials_file_path, "w") as file:
            file.write(api_id + "\n")
            file.write(api_hash + "\n")
            file.write(phone_number)

    @staticmethod
    def write_chats(phone_number, dialogs):
        chats_file = open(FileOperation.chats_file_path, "w")
        print(f"Chats for phone number: {phone_number}")
        chats_file.write(f"phone number: {phone_number}\n")
        for dialog in dialogs:
            chat_type = "UNKNOWN"
            if (dialog.is_channel):
                chat_type = "channel"
            elif (dialog.is_group):
                chat_type = "group"
            elif (dialog.is_user):
                chat_type = "user"
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}, Type: {chat_type}")
            chats_file.write(f"Chat ID: {dialog.id}, Title: {dialog.title}, Type: {chat_type}\n")

    @staticmethod
    def read_forward_config():
        try:
            with open(FileOperation.forward_config_file_path, "r") as file:
                lines = file.readlines()
                source =  int(lines[0].strip())
                destination =  int(lines[1].strip())
                delay = int(lines[2].strip())
                keywords = lines[3].strip()
                return source, destination, delay, keywords
        except Exception:
            return None, None, None, None

    @staticmethod
    def write_forward_config(source, destination, delay, keywords):
        with open(FileOperation.forward_config_file_path, "w") as file:
            file.write(f"{source}\n")
            file.write(f"{destination}\n")
            file.write(f"{delay}\n")
            file.write(', '.join(keywords) + "\n")
