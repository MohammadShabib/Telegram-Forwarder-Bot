import json
import os
from InquirerPy import inquirer

class Credentials:
    CREDENTIALS_FILE = "resources/credentials.json"

    def __init__(self, api_id=None, api_hash=None, phone_number=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

    @staticmethod
    async def get(use_existing=True):
        if use_existing and os.path.exists(Credentials.CREDENTIALS_FILE):
            with open(Credentials.CREDENTIALS_FILE, 'r') as f:
                credentials = json.load(f)
                if credentials:  # Return first account if just wanting to use existing
                    cred = credentials[0]
                    return Credentials(
                        api_id=cred['api_id'],
                        api_hash=cred['api_hash'],
                        phone_number=cred['phone_number']
                    )
        
        # If no existing credentials or explicitly asking for new
        new_credentials = await Credentials._get_credentials_from_user()
        Credentials._save_credentials(new_credentials.__dict__)
        return new_credentials

    @staticmethod
    def get_all():
        if os.path.exists(Credentials.CREDENTIALS_FILE):
            with open(Credentials.CREDENTIALS_FILE, 'r') as f:
                creds_list = json.load(f)
                return [Credentials(
                    api_id=cred['api_id'],
                    api_hash=cred['api_hash'],
                    phone_number=cred['phone_number']
                ) for cred in creds_list]
        return []

    @staticmethod
    async def _get_credentials_from_user():
        api_id = await inquirer.text(message="Enter API ID:").execute_async()
        api_hash = await inquirer.text(message="Enter API Hash:").execute_async()
        phone_number = await inquirer.text(message="Enter Phone Number:").execute_async()
        
        return Credentials(
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number
        )

    @staticmethod
    def _save_credentials(new_credentials_dict):
        existing = []
        if os.path.exists(Credentials.CREDENTIALS_FILE):
            with open(Credentials.CREDENTIALS_FILE, 'r') as f:
                existing = json.load(f)
        
        existing.append(new_credentials_dict)
        
        os.makedirs(os.path.dirname(Credentials.CREDENTIALS_FILE), exist_ok=True)
        with open(Credentials.CREDENTIALS_FILE, 'w') as f:
            json.dump(existing, f, indent=2)
