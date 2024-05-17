import asyncio

from InquirerPy import inquirer

from source.telegram.Telegram import Telegram
from source.model.Credentials import Credentials
from source.model.ForwardConfig import ForwardConfig
from source.utils.Console import Terminal


class Bot:
    def __init__(self):
        self.telegram = Telegram(Credentials.get(True))

    options = [
        {"name": "Add/Update Credentials", "value": "1"},
        {"name": "List Chats", "value": "2"},
        {"name": "Forward Messages", "value": "3"},
        {"name": "Exit", "value": "0"}
    ]
    console = Terminal.console

    async def start(self):
        try:
            while True:
                choice = await inquirer.select(
                    message="Menu:",
                    choices=Bot.options).execute_async()
                if choice == "0":
                    Terminal.console.print("[bold red]Exiting...[/bold red]")
                    break
                elif choice == "1":
                    await self.update_credentials()

                if choice == "2":
                    await self.list_chats()

                elif choice == "3":
                    await self.start_forward()

                else:
                    self.console.print("[bold red]Invalid choice[/bold red]")
        except Exception as err:
            raise err
        finally:
            self.telegram.client.disconnect()


    async def update_credentials(self):
        self.console.clear()
        self.telegram.client.disconnect()
        self.telegram = Telegram(Credentials.get(False))

    async def list_chats(self):
        self.console.clear()
        await self.telegram.list_chats()

    async def start_forward(self):
        forwardConfigList = await ForwardConfig.getAll(True)
        forwardConfigString = '\n   '.join(str(forwardConfig) for forwardConfig in forwardConfigList)
        forward_options = [
            {
                "name": "Use saved settings.\n   " + forwardConfigString,
                "value": "1"
            },
            {
                "name": "New settings",
                "value": "2"
            }
        ]

        forward_choice = await inquirer.select(
            message="Forward Settings:",
            choices=forward_options
        ).execute_async()

        if forward_choice == "2":
            forwardConfigList = await ForwardConfig.getAll(False)

        forwardConfigMap = {item.sourceID: item for item in forwardConfigList}
        await self.telegram.start_forward(forwardConfigMap)
