from source.dialog.BaseDialog import BaseDialog
from source.model.Chat import Chat

class FindUserDialog(BaseDialog):
    async def get_config(self):
        """Get user tracking configuration.
        
        Returns:
            Chat: Selected user to track
        """
        self.clear()
        return await self._get_wanted_user()

    async def _get_wanted_user(self):
        """Get wanted user configuration.
        
        Returns:
            Chat: Selected user to track
        """
        chats = Chat.read_wanted_users()
        options = [{"name": "➕ Add New User", "value": "new"}]
        
        # Show existing tracked users
        for i, chat in enumerate(chats):
            options.append({
                "name": chat.get_plain_display_name(),
                "value": str(i)
            })

        choice = await self.show_options("Select target user:", options)
        
        if choice == "new":
            all_chats = Chat.read()
            new_choice = await self.list_chats_terminal(all_chats, "target")
            if new_choice == -1:
                return None
            selected_user = all_chats[new_choice]
            chats.append(selected_user)
            Chat.write_wanted_users(chats)  # Save all users including the new one
            return selected_user
            
        return chats[int(choice)] 