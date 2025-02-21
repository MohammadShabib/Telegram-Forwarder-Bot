from source.menu.AccountSelector import AccountSelector
from source.menu.MainMenu import MainMenu

class Bot:
    def __init__(self):
        self.account_selector = AccountSelector()
        self.main_menu = None

    async def start(self):
        try:
            telegram = await self.account_selector.select_account()
            self.main_menu = MainMenu(telegram)
            await self.main_menu.start()
        except Exception as err:
            raise err


