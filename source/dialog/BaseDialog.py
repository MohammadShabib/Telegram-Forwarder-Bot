from InquirerPy import inquirer
from source.utils.Console import Terminal
from rich.markup import render

class BaseDialog:
    def __init__(self):
        self.console = Terminal.console

    async def show_options(self, message, options):
        return await inquirer.select(message=message, choices=options).execute_async()

    def clear(self):
        self.console.clear()

    async def list_chats_terminal(self, chats, type_label):
        """Shows a list of chats for selection."""
        options = [{"name": "Stop", "value": "-1"}]
        
        for i, chat in enumerate(chats):
            options.append({
                "name": chat.get_plain_display_name(),
                "value": str(i)
            })

        choice = await self.show_options(f"Enter {type_label} channel", options)
        return int(choice) 