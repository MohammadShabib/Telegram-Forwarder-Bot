import os
from telethon import TelegramClient
from telethon.tl.custom import Dialog
from telethon.tl.types import Message, User, Chat, Channel
from telethon.errors import ChatAdminRequiredError
from source.utils.Constants import MEDIA_FOLDER_PATH
from source.utils.Console import Terminal
from typing import Optional, Union

class MessageService:
    """Service for handling Telegram message operations.
    
    This class provides functionality for message deletion, processing user messages,
    and handling media downloads.
    
    Attributes:
        client (TelegramClient): The Telegram client instance
        console (Console): Rich console instance for output
        chat_service (ChatService): Service for chat-related operations
    """

    def __init__(self, client: TelegramClient, console: Optional[Terminal] = None):
        self.client = client
        self.console = console or Terminal.console
        self.chat_service = None  # Will be set by Telegram class

    async def delete_messages_from_dialog(self, dialog: Dialog, my_id: int) -> None:
        """Deletes user's messages from a specific dialog.
        
        Args:
            dialog: Telegram dialog to delete messages from
            my_id: ID of the user whose messages should be deleted
        """
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

    async def process_user_messages(self, chat: Union[User, Chat, Channel], wanted_user: User, limit: int = None) -> None:
        """Processes messages from a specific user in a chat.
        
        Downloads media and displays message information for messages
        from the specified user.
        
        Args:
            chat: Telegram chat entity to process (User, Chat, or Channel)
            wanted_user: User entity whose messages should be processed
            limit: Maximum number of messages to process per chat
        """
        try:
            message_count = 0
            async for message in self.client.iter_messages(chat, from_user=wanted_user, limit=limit):
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
                self.console.print(
                    f"[bold green]✨ FOUND {message_count} MESSAGES IN {self.chat_service.get_chat_name(chat).upper()}! ✨\n\n[/bold green]")

        except ChatAdminRequiredError:
            self.console.print(f"[yellow]No access to {self.chat_service.get_chat_name(chat)}[/yellow]")
        except Exception as e:
            if "private" not in str(e).lower() and "banned" not in str(e).lower():
                self.console.print(f"[red]Error processing {self.chat_service.get_chat_name(chat)}: {e}[/red]")

    async def download_media(self, message: Message) -> Optional[str]:
        """Downloads media from a message.
        
        Args:
            message: Telegram message containing media
            
        Returns:
            str: Path to downloaded media file, or None if download failed
        """
        os.makedirs(MEDIA_FOLDER_PATH, exist_ok=True)
        return await self.client.download_media(message, file=MEDIA_FOLDER_PATH) 