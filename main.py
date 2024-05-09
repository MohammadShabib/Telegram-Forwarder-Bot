import asyncio
import os

from source.Bot import Bot
from source.utils.Console import Terminal

console = Terminal.console

def main():
    try:
        os.makedirs("resources", exist_ok=True)
        bot = Bot()
        if asyncio.get_event_loop().is_running():
            console.print("[bold yellow]Using the existing event loop.[/bold yellow]")
            asyncio.ensure_future(bot.start())
        else:
            console.print("[bold yellow]Starting a new event loop.[/bold yellow]")
            asyncio.run(bot.start())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    main()
