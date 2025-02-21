from InquirerPy import inquirer
from source.utils.Console import Terminal

class BaseDialog:
    def __init__(self):
        self.console = Terminal.console

    async def show_options(self, message, options):
        return await inquirer.select(message=message, choices=options).execute_async()

    def clear(self):
        self.console.clear() 