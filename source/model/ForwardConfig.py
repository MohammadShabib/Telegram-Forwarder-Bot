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

    @staticmethod
    def write(forwardConfigList):
        forwardList = []
        for _ in forwardConfigList:
            forwardList.append(_.__dict__)
        with open(ForwardConfig.file_path, "w") as file:
            json.dump(forwardList, file, indent=4)

    @staticmethod
    def read():
        with open(ForwardConfig.file_path, "r") as file:
            data = json.load(file)
            return [ForwardConfig(**forwardConfig) for forwardConfig in data]

    @staticmethod
    async def scan():
        chat = Chat()
        chats = chat.read()
        forwardConfigList = []
        while True:
            forwardConfig = ForwardConfig()
            sourceChoice = await Utilities.list_chats_terminal(chats, "source")
            if (sourceChoice == -1):
                break
            source = chats[sourceChoice]
            forwardConfig.sourceID = source.id
            forwardConfig.sourceName = source.title

            destinationChoice = await Utilities.list_chats_terminal(chats, "destination")
            destination = chats[destinationChoice]
            forwardConfig.destinationID = destination.id
            forwardConfig.destinationName = destination.title

            forwardConfig.delay = int(input("Enter delay time between checking chats in seconds: "))
            forwardConfigList.append(forwardConfig)
        ForwardConfig.write(forwardConfigList)
        return forwardConfigList

    @staticmethod
    async def getAll(is_saved=True):
        if is_saved and os.path.exists(ForwardConfig.file_path):
            return ForwardConfig.read()
        else:
            return await ForwardConfig.scan()

    def __repr__(self):
        return (f'sourceName= "{self.sourceName}", destinationName= "{self.destinationName}", delay= {self.delay}')
