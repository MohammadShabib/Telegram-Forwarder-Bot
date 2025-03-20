from InquirerPy import inquirer
from source.utils.Console import Terminal
from source.model.Credentials import Credentials
from source.core.Telegram import Telegram

class AccountSelector:
    def __init__(self):
        self.console = Terminal.console

    async def select_account(self):
        credentials_list = Credentials.get_all()
        
        if not credentials_list:
            self.console.print("[bold red]No credentials found. Please add credentials first.[/bold red]")
            credentials = await Credentials.get(False)
            return await Telegram.create(credentials)

        choices = [
            {
                "name": f"Account: {cred.phone_number}",
                "value": cred
            } for cred in credentials_list
        ]
        
        choices.append({
            "name": "➕ Add New Account",
            "value": "new"
        })
        
        selected = await inquirer.select(
            message="Select account to use:",
            choices=choices
        ).execute_async()
        
        if selected == "new":
            credentials = await Credentials.get(False)
            return await Telegram.create(credentials)
        
        return await Telegram.create(selected) 