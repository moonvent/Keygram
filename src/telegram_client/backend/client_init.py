"""
    Client initialization
"""

import asyncio
import os
from threading import Thread
from typing import Coroutine
from telethon.hints import TotalList
from telethon.tl.patched import Message

from telethon.tl.types import Dialog, User
from src.services import load_env_vars              # for load env vars from .env file
import time
from telethon import TelegramClient, custom, events, sync
import functools


api_id = str(os.environ['API_ID'])
api_hash = str(os.environ['API_HASH'])


class CustomTelegramClient:
    """
        Custom class for tg client, for work in other thread
    """
    client: TelegramClient = None
    loop: asyncio.AbstractEventLoop = None
    
    media_to_download: list[tuple[str, Message], ...] = []
    need_to_load: bool = False
    
    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.client = TelegramClient('session_name', int(api_id), api_hash)
        self.client.start()

    def async_function():
        """
            Decorators for add loop until complete, for not writing async in other code files
        """
        def wrapper(func):
            @functools.wraps(func) 
            def wrapped(self, *args, **kwargs):
                return self.loop.run_until_complete(func(self, *args, **kwargs))
            return wrapped
        return wrapper

    @async_function()
    async def get_me(self):
        return await self.client.get_me()

    @async_function()
    async def get_dialogs(self, limit: int, offset: int = 0):
        return await self.client.get_dialogs(limit=limit,
                                             offset_id=offset)

    @async_function()
    async def download_profile_photo(self, dialog_id: int, avatar_path: str):
        return await self.client.download_profile_photo(dialog_id,
                                                        avatar_path)

    @async_function()
    async def get_messages(self, chat_id, limit):
        return await self.client.get_messages(chat_id, limit)

    @async_function()
    async def download_media(self, message, path, thumb: bool = False):
        if not thumb:
            return await self.client.download_media(message, path)
        else:
            return await self.client.download_media(message, path, thumb=-1)

    @async_function()
    async def download_all_media(self, start_media_path: str = None):
        # if start_media_path:
        #     await self.client.download_media(self.media_to_download[start_media_path], start_media_path)

        # self.client.download_media(self.media_to_download[start_media_path], start_media_path)

        while True:
            if self.media_to_download:
                path, message = self.media_to_download.pop(0)
                if not os.path.exists(path):
                    await self.client.download_media(message, path)

            if not self.check_need_to_load_static():
                time.sleep(1)

    def check_need_to_load_static(self) -> bool:
        """
            Search if need to load new data
        """
        return any(not os.path.exists(path) for path, message in self.media_to_download)

    def add_to_downloads(self, message: Message, path: str):
        self.media_to_download.append((path, message))


client: CustomTelegramClient = None


def start_client():
    custom_client = CustomTelegramClient()
    global client
    client = custom_client


tg_client_thread = Thread(target=start_client, daemon=True)
tg_client_thread.start()
time.sleep(2)

