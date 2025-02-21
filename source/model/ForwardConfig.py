import json
import os.path

from source.model.Chat import Chat
from source.utils.Constants import FORWARD_CONFIG_FILE_PATH
from source.dialog.BaseDialog import BaseDialog


class ForwardConfig:

    def __init__(self, sourceID=None, sourceName=None, destinationID=None, destinationName=None):
        self.sourceID = sourceID
        self.sourceName = sourceName
        self.destinationID = destinationID
        self.destinationName = destinationName

    @staticmethod
    def write(forward_config_list):
        forwardList = []
        for _ in forward_config_list:
            forwardList.append(_.__dict__)
        with open(FORWARD_CONFIG_FILE_PATH, "w") as file:
            json.dump(forwardList, file, indent=4)

    @staticmethod
    def read():
        with open(FORWARD_CONFIG_FILE_PATH, "r") as file:
            data = json.load(file)
            return [ForwardConfig(**forwardConfig) for forwardConfig in data]

    @staticmethod
    async def scan():
        chat = Chat()
        chats = chat.read()
        forwardConfigList = []
        dialog = BaseDialog()
        
        while True:
            forwardConfig = ForwardConfig()
            sourceChoice = await dialog.list_chats_terminal(chats, "source")
            if sourceChoice == -1:
                break
            source = chats[sourceChoice]
            forwardConfig.sourceID = source.id
            forwardConfig.sourceName = source.title

            destinationChoice = await dialog.list_chats_terminal(chats, "destination")
            destination = chats[destinationChoice]
            forwardConfig.destinationID = destination.id
            forwardConfig.destinationName = destination.title

            forwardConfigList.append(forwardConfig)
        ForwardConfig.write(forwardConfigList)
        return forwardConfigList

    @staticmethod
    async def get_all(is_saved=True):
        if is_saved and os.path.exists(FORWARD_CONFIG_FILE_PATH):
            return ForwardConfig.read()
        else:
            return await ForwardConfig.scan()

    def __repr__(self):
        return f'sourceName= "{self.sourceName}", destinationName= "{self.destinationName}"'
