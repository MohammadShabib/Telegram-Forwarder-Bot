import asyncio
import os
import signal
import sys

from source.Bot import Bot
from source.utils.Console import Terminal

console = Terminal.console


async def shutdown(loop, signal=None):
    if signal:
        print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    print(f"Cancelling {len(tasks)} tasks...")
    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def main():
    os.makedirs("resources", exist_ok=True)
    bot = Bot()
    try:
        loop = asyncio.get_event_loop()
        if sys.platform != 'win32':
            signals = (signal.SIGINT, signal.SIGTERM)
            for s in signals:
                loop.add_signal_handler(s, lambda a=s: asyncio.create_task(shutdown(loop, signal=s)))
        loop.run_until_complete(bot.start())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
