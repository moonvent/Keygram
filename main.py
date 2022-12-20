import asyncio
from src.telegram_client.backend.dialogs.dialogs import get_dialogs
from src.telegram_client.frontend.gui import start_gui


async def main():
    await get_dialogs([])


def test():
    print('test')


if __name__ == "__main__":
    # current_event_loop = asyncio.get_event_loop()
    # current_event_loop.run_until_complete(main())
    start_gui()

