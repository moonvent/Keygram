"""
    Get dialogs data from api   
"""

from telethon import functions
from telethon.hints import TotalList
from src.telegram_client.backend.client_init import client
from src.config import DIALOGS_LOAD_LIMIT
from src.telegram_client.backend.dialogs.download_avatars import download_avatars



async def get_dialogs(dialogs_list: list, offset: int = 0):
    """
        Get dialogs with amount DIALOGS_LOAD_LIMIT and offset
        :param dialogs_list: list of dialogs for gui WITH peers (for seen status)
        :param offset: offset for getting new dialogs
    """
    dialogs = await client.get_dialogs(limit=DIALOGS_LOAD_LIMIT,
                                       offset_id=offset)
    await download_avatars(dialogs=dialogs)

    # dialogs_ids = tuple(dialog.id for dialog in dialogs)
    #
    # peer_dialogs_pre_handled = await client(functions.messages.GetPeerDialogsRequest(
    #     peers=dialogs_ids
    # ))
    #
    # peer_dialogs = []
    # 
    # for peer_dialog in zip(peer_dialogs_pre_handled.chats, 
    #                        peer_dialogs_pre_handled.dialogs,
    #                        peer_dialogs_pre_handled.messages,
    #                        peer_dialogs_pre_handled.users,
    #                        ):
    #     peer_dialogs.append(peer_dialog)
    # 
    # dialogs_list += list(zip(dialogs, peer_dialogs))
    
    dialogs_list += dialogs
