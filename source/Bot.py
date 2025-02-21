from InquirerPy import inquirer

from source.telegram.Telegram import Telegram
from source.model.Credentials import Credentials
from source.model.ForwardConfig import ForwardConfig
from source.utils.Console import Terminal
from source.model.Chat import Chat
from source.dialog.ForwardDialog import ForwardDialog
from source.dialog.DeleteDialog import DeleteDialog
from source.dialog.FindUserDialog import FindUserDialog


class Bot:
    def __init__(self):
        self.telegram = Telegram(Credentials.get(True))
        self.console = Terminal.console
        self.menu_options = self._init_menu_options()
        self.forward_dialog = ForwardDialog()
        self.delete_dialog = DeleteDialog()
        self.find_user_dialog = FindUserDialog()

    def _init_menu_options(self):
        return [
            {"name": "Add/Update Credentials", "value": "1", "handler": self.update_credentials},
            {"name": "List Chats", "value": "2", "handler": self.list_chats},
            {"name": "Live Forward Messages", "value": "3", "handler": self.live_forward},
            {"name": "Past Forward Messages", "value": "4", "handler": self.past_forward},
            {"name": "Delete My Messages", "value": "5", "handler": self.delete_messages},
            {"name": "Find User Messages", "value": "6", "handler": self.find_user},
            {"name": "Exit", "value": "0", "handler": None}
        ]

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
        except Exception as err:
            raise err
        finally:
            await self._cleanup()

    async def _get_menu_choice(self):
        choices = [{"name": opt["name"], "value": opt["value"]} for opt in self.menu_options]
        return await inquirer.select(message="Menu:", choices=choices).execute_async()

    async def _cleanup(self):
        await self.telegram.client.disconnect()

    async def update_credentials(self):
        self.console.clear()
        await self.telegram.client.disconnect()
        self.telegram = Telegram(Credentials.get(False))

    async def list_chats(self):
        self.console.clear()
        await self.telegram.list_chats()

    async def live_forward(self):
        config = await self.forward_dialog.get_config()
        await self.telegram.start_forward(config[0])

    async def past_forward(self):
        config = await self.forward_dialog.get_config()
        await self.telegram.past(config[0])

    async def delete_messages(self):
        ignore_chats = await self.delete_dialog.get_config()
        await self.telegram.delete(ignore_chats)

    async def find_user(self):
        wanted_user = await self.find_user_dialog.get_config()
        await self.telegram.findUser(wanted_user)


