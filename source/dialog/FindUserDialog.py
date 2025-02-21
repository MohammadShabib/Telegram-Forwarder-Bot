from source.dialog.BaseDialog import BaseDialog
from source.model.Chat import Chat

class FindUserDialog(BaseDialog):
    async def get_config(self):
        self.clear()
        return await self._get_wanted_user()

    async def _get_wanted_user(self):
        wanted_user = await Chat.get_wanted_user(True)
        options = [
            {"name": f"Use saved target user.\n   {wanted_user.type}: {wanted_user.title}", "value": "1"},
            {"name": "New target user", "value": "2"}
        ]

        choice = await self.show_options("Target User Settings:", options)
        if choice == "2":
            wanted_user = await Chat.get_wanted_user(False)
        
        return wanted_user 