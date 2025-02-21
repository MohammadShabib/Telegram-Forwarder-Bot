import os
import telethon
from source.utils.Constants import MEDIA_FOLDER_PATH
from source.utils.Console import Terminal

class MessageService:
    def __init__(self, client, console=None):
        self.client = client
        self.console = console or Terminal.console
        self.chat_service = None  # Will be set by Telegram class

    async def delete_messages_from_dialog(self, dialog, my_id):
        """Deletes user's messages from a specific dialog."""
        chat = dialog.entity
        try:
            self.console.print(f"[bold]Searching in[/bold] [blue]{self.chat_service.get_chat_name(chat)}[/blue]")
            deleted_count = 0
            async for message in self.client.iter_messages(chat, from_user=my_id):
                
                if message.text:
                    self.console.print(f"[dim]Deleting:[/dim] [white]{message.text[:100]}{'...' if len(message.text) > 100 else ''}[/white]")

                await self.client.delete_messages(chat, message.id)
                deleted_count += 1
                if deleted_count % 10 == 0:  # Progress update every 10 messages
                    self.console.print(f"[green]Deleted {deleted_count} messages...[/green]")
            
            if deleted_count > 0:
                self.console.print(f"[bold green]✓ Successfully deleted {deleted_count} messages[/bold green]")
                
        except Exception as e:
            self.console.print(f"[bold red]Error deleting messages: {e}[/bold red]")

    async def process_user_messages(self, chat, user_id):
        """Processes messages from a specific user in a chat."""
        try:
            message_count = 0
            async for message in self.client.iter_messages(chat, from_user=user_id):
                message_count += 1
                self.chat_service.print_chat_info(chat, message)
                
                if message.media:
                    try:
                        file_path = await self.download_media(message)
                        if file_path:
                            self.console.print(f"[green]📎 Media downloaded to:[/green] {file_path}")
                    except Exception as e:
                        self.console.print(f"[yellow]Failed to download media: {e}[/yellow]")

            if message_count > 0:
                self.console.print(f"[green]Found {message_count} messages in {self.chat_service.get_chat_name(chat)}[/green]")

        except telethon.errors.ChatAdminRequiredError:
            self.console.print(f"[yellow]No access to {self.chat_service.get_chat_name(chat)}[/yellow]")
        except Exception as e:
            if "private" not in str(e).lower() and "banned" not in str(e).lower():
                self.console.print(f"[red]Error processing {self.chat_service.get_chat_name(chat)}: {e}[/red]")

    async def download_media(self, message):
        """Downloads media from a message."""
        os.makedirs(MEDIA_FOLDER_PATH, exist_ok=True)
        return await self.client.download_media(message, file=MEDIA_FOLDER_PATH) 