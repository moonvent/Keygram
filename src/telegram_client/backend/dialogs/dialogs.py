"""
    Get dialogs data from api   
"""

from random import randint
from telethon import functions
from telethon.hints import TotalList
from src.telegram_client.backend.client_init import client
from src.config import DIALOGS_LOAD_LIMIT
from src.telegram_client.backend.dialogs.download_avatars import download_avatars



def get_dialogs(offset: int = 0):
    """
        Get dialogs with amount DIALOGS_LOAD_LIMIT and offset
        :param dialogs_list: list of dialogs for gui WITH peers (for seen status)
        :param offset: offset for getting new dialogs
    """
    dialogs = client.get_dialogs()
    download_avatars(dialogs=dialogs)
    return dialogs
