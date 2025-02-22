from InquirerPy import inquirer
from source.utils.Console import Terminal
from source.model.Credentials import Credentials
from source.core.Telegram import Telegram
from source.dialog.ForwardDialog import ForwardDialog
from source.dialog.DeleteDialog import DeleteDialog
from source.dialog.FindUserDialog import FindUserDialog
from source.menu.AccountSelector import AccountSelector

class MainMenu:
    def __init__(self, telegram):
        self.console = Terminal.console
        self.telegram = telegram
        self.menu_options = self._init_menu_options()
        self.forward_dialog = ForwardDialog()
        self.delete_dialog = DeleteDialog()
        self.find_user_dialog = FindUserDialog()

    def _init_menu_options(self):
        return [
            {"name": "Add/Update Credentials", "value": "1", "handler": self.update_credentials},
            {"name": "List Chats", "value": "2", "handler": self.list_chats},
            {"name": "Delete My Messages", "value": "3", "handler": self.delete_messages},
            {"name": "Find User Messages", "value": "4", "handler": self.find_user},
            {"name": "Live Forward Messages", "value": "5", "handler": self.live_forward},
            {"name": "Past Forward Messages", "value": "6", "handler": self.past_forward},
            {"name": "Switch Account", "value": "7", "handler": self.switch_account},
            {"name": "Exit", "value": "0", "handler": None}
        ]

    async def _get_menu_choice(self):
        choices = [{"name": opt["name"], "value": opt["value"]} for opt in self.menu_options]
        return await inquirer.select(message="Menu:", choices=choices).execute_async()

    async def start(self):
        try:
            while True:
                choice = await self._get_menu_choice()
                if choice == "0":
                    self.console.print("[bold red]Exiting...[/bold red]")
                    break
                
                handler = next(opt["handler"] for opt in self.menu_options if opt["value"] == choice)
                if handler:
                    await handler()
                else:
                    self.console.print("[bold red]Invalid choice[/bold red]")
        finally:
            if self.telegram:
                await self._cleanup()

    async def _cleanup(self):
        if self.telegram:
            await self.telegram.disconnect()

    async def update_credentials(self):
        self.console.clear()
        await self.telegram.disconnect()
        self.telegram = await Telegram.create(Credentials.get(False))

    async def list_chats(self):
        self.console.clear()
        await self.telegram.list_chats()

    async def live_forward(self):
        config = await self.forward_dialog.get_config()
        await self.telegram.start_forward_live(config)

    async def past_forward(self):
        config = await self.forward_dialog.get_config()
        await self.telegram.past_forward(config)

    async def delete_messages(self):
        ignore_chats = await self.delete_dialog.get_config()
        await self.telegram.delete(ignore_chats)

    async def find_user(self):
        config = await self.find_user_dialog.get_config()
        await self.telegram.find_user(config)

    async def switch_account(self):
        await self._cleanup()
        selector = AccountSelector()
        self.telegram = await selector.select_account() 