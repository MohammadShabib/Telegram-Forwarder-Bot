from source.dialog.BaseDialog import BaseDialog
from source.model.Chat import Chat

class DeleteDialog(BaseDialog):
    async def get_config(self):
        self.clear()
        return await self._get_ignore_chats()

    async def _get_ignore_chats(self):
        ignore_chats = await Chat.get_ignore_chats(True)
        ignore_string = '\n   '.join(f"{chat.type}: {chat.title}" for chat in ignore_chats)
        
        options = [
            {"name": "Use saved ignore list.\n   " + ignore_string, "value": "1"},
            {"name": "New ignore list", "value": "2"}
        ]

        choice = await self.show_options("Ignore Settings:", options)
        if choice == "2":
            ignore_chats = await Chat.get_ignore_chats(False)
        
        return ignore_chats 