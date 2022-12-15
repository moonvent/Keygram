from telethon.hints import TotalList
from src.telegram_client.backend.client_init import client
from src.telegram_client.backend.config import DIALOGS_LOAD_LIMIT
from src.telegram_client.backend.dialogs.download_avatars import download_avatars



async def get_dialogs(dialogs_list: list, offset: int = 0):
    """
        Get dialogs with amount DIALOGS_LOAD_LIMIT and offset
        :param dialogs_list: list of dialogs for gui
        :param offset: offset for getting new dialogs
    """
    dialogs = await client.get_dialogs(limit=DIALOGS_LOAD_LIMIT,
                                       offset_id=offset)
    await download_avatars(dialogs=dialogs)

    dialogs_list += dialogs

