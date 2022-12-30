"""
    Client initialization
"""

import asyncio
import os
from threading import Thread
from typing import Coroutine, NamedTuple
from telethon.hints import TotalList
from telethon.tl.patched import Message

from telethon.tl.types import Dialog, User
from src.config import SPEED_STEP, SettingsEnum
from src.services.database.models.global_data import get_settings
from src.services import load_env_vars              # for load env vars from .env file
import time
from telethon import TelegramClient, custom, events, sync
import functools

from src.telegram_client.backend.chat.video_widget import fastify_video


api_id = str(os.environ['API_ID'])
api_hash = str(os.environ['API_HASH'])


class DownloadFile(NamedTuple):
    path: str
    message: Message
    speed: float


class CustomTelegramClient:
    """
        Custom class for tg client, for work in other thread
    """
    client: TelegramClient = None
    loop: asyncio.AbstractEventLoop = None
    
    media_to_download: list[DownloadFile, ...] = []
    need_to_load: bool = False

    download_cycle: bool = False
    
    def __init__(self) -> None:
        self.recreate_loop()

        self.client = TelegramClient('session_name', int(api_id), api_hash)
        self.client.start()

    def recreate_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    # попробуй сделать отдельно луп и в него сувать задачки

    def async_function():
        """
            Decorators for add loop until complete, for not writing async in other code files
        """
        def wrapper(func):
            @functools.wraps(func) 
            def wrapped(self, *args, **kwargs):
                # if self.loop.is_running():
                #     self.recreate_loop()
                # if 'download_all_task' in args:
                #     asyncio.gather(func(self, *args, **kwargs))
                # else:
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
    async def download_all_media(self):
        while True:
            print(self.media_to_download)
            if self.media_to_download:
                download_file: DownloadFile = self.media_to_download.pop(0)
                if not os.path.exists(download_file.path):
                    await self.client.download_media(download_file.message, download_file.path)
                    # Thread(target=fastify_video, 
                    #        args=(download_file.path, download_file.speed)).start()

            if not self.check_need_to_load_static():
                print('wait to media')
                await asyncio.sleep(1)
        print('end')

    def check_need_to_load_static(self) -> bool:
        """
            Search if need to load new data
        """
        return any(not os.path.exists(download_file.path) for download_file in self.media_to_download)

    def add_to_downloads(self, message: Message, path: str, speed: int):
        # self.media_to_download.append((path, message, speed))
        self.media_to_download.append(DownloadFile(path, message, speed))


client: CustomTelegramClient = None




def start_client():
    custom_client = CustomTelegramClient()
    global client
    client = custom_client


tg_client_thread: Thread = Thread(target=start_client, daemon=True)
tg_client_thread.start()

while not client:
    ...

# time.sleep(2)
