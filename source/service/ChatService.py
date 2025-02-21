from source.utils.Console import Terminal
import telethon

class ChatService:
    def __init__(self, console=None):
        self.console = console or Terminal.console

    @staticmethod
    def get_chat_name(chat):
        """Get a formatted chat name, preferring username if available."""
        try:
            if hasattr(chat, 'title') and chat.title:
                return chat.title
            if hasattr(chat, 'username') and chat.username:
                return f"@{chat.username}"
            if hasattr(chat, 'first_name'):
                name_parts = []
                if chat.first_name:
                    name_parts.append(chat.first_name)
                if hasattr(chat, 'last_name') and chat.last_name:
                    name_parts.append(chat.last_name)
                return " ".join(name_parts)
            return "Unknown Chat"
        except Exception:
            return "Unknown Chat"

    @staticmethod
    def get_chat_type(chat):
        """Get chat type with proper error handling."""
        try:
            if isinstance(chat, telethon.tl.types.User):
                return "👤 User"
            if hasattr(chat, 'megagroup') and chat.megagroup:
                return "👥 Group"
            if hasattr(chat, 'broadcast') and chat.broadcast:
                return "📢 Channel"
            if hasattr(chat, 'is_group') and chat.is_group:
                return "👥 Group"
            return "💬 Chat"
        except Exception:
            return "💬 Chat"

    def print_chat_info(self, chat, message=None):
        """Print formatted chat information."""
        chat_name = self.get_chat_name(chat)
        chat_type = self.get_chat_type(chat)
        
        self.console.print(f"[bold blue]{chat_type}[/bold blue]: [yellow]{chat_name}[/yellow]")
        if message:
            self.console.print(f"[dim]Date:[/dim] [cyan]{message.date}[/cyan]")
            if message.text:
                self.console.print(f"[dim]Message:[/dim] [white]{message.text}[/white]")
            if hasattr(message.peer_id, 'channel_id'):
                link = f"https://t.me/c/{message.peer_id.channel_id}/{message.id}"
                self.console.print(f"[dim]Link:[/dim] [link]{link}[/link]")
            self.console.print("─" * 50) 