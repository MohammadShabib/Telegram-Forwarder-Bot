import json
import os.path

from source.model.Chat import Chat
from source.utils.Utilities import Utilities


class ForwardConfig:
    file_path = "resources/forwardConfig.json"

    def __init__(self, sourceID=None, sourceName=None, destinationID=None, destinationName=None, delay=None):
        self.sourceID = sourceID
        self.sourceName = sourceName
        self.destinationID = destinationID
        self.destinationName = destinationName
        self.delay = delay

    def write(self):
        with open(self.file_path, "w") as file:
            json.dump(self.__dict__, file, indent=4)

    @staticmethod
    def read():
        with open(ForwardConfig.file_path, "r") as file:
            data = json.load(file)
            return ForwardConfig(**data)

    @staticmethod
    async def scan():
        chat = Chat()
        chats = chat.read()
        forwardConfig = ForwardConfig()
        source = await Utilities.list_chats_terminal(chats, "source")
        forwardConfig.sourceID = source.id
        forwardConfig.sourceName = source.title

        destination = await Utilities.list_chats_terminal(chats, "destination")
        forwardConfig.destinationID = destination.id
        forwardConfig.destinationName = destination.title

        forwardConfig.delay = int(input("Enter delay time between checking chats in seconds: "))
        forwardConfig.write()
        return forwardConfig

    @staticmethod
    async def get(is_saved=True):
        if is_saved and os.path.exists(ForwardConfig.file_path):
            return ForwardConfig.read()
        else:
            return await ForwardConfig.scan()