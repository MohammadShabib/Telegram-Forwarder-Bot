import json
import os.path

from source.utils.Constants import CREDENTIALS_FILE_PATH


class Credentials:

    def __init__(self, api_id=None, api_hash=None, phone_number=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

    def write(self):
        with open(CREDENTIALS_FILE_PATH, "w") as file:
            json.dump(self.__dict__, file, indent=4)

    @staticmethod
    def read():
        with open(CREDENTIALS_FILE_PATH, "r") as file:
            data = json.load(file)
            return Credentials(**data)

    @staticmethod
    def scan():
        credentials = Credentials()
        credentials.api_id = input("Enter your API ID: ")
        credentials.api_hash = input("Enter your API Hash: ")
        credentials.phone_number = input("Enter your phone number: ")
        credentials.write()
        return credentials

    @staticmethod
    def get(is_saved=False):
        if is_saved and os.path.exists(CREDENTIALS_FILE_PATH):
            return Credentials.read()
        else:
            return Credentials.scan()
