from InquirerPy import inquirer


class Utilities:

    @staticmethod
    async def list_chats_terminal(chats, type):
        forward_options = []
        forward_options.append({"name": "Stop", "value": "-1"})
        i = 0
        for chat in chats:
            forward_option = {}
            forward_option['name'] = f'{chat.type}: {chat.title}'
            forward_option['value'] = f'{i}'
            forward_options.append(forward_option)
            i += 1


        forward_choice = int(await inquirer.select(
            message=f"Enter {type} channel",
            choices=forward_options
        ).execute_async())
        return forward_choice
