"""
    File for download all media in background 
    NOW NOT WORK
"""
import asyncio
import os
from threading import Thread
import time
from PySide6.QtCore import QThread
from loguru import logger
from src.services.logging.setup_logger import logger, create_exception_log
from src.telegram_client.backend.client_init import client

from telethon.tl.patched import Message

from src.config import VIDEO_MESSAGE_PATH


message_with_media_to_load: list[tuple[str, Message]] = []


async def load_media_async():
    while True:

        try:
            if message_with_media_to_load:
                path_to_file, message = message_with_media_to_load.pop()
                print(path_to_file)
                await client.download_media(message, path_to_file)
                print('loaded')
                # await asyncio.sleep(.3)

        except:
            create_exception_log()


# def load_media():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#
#     loop.run_until_complete(load_media())
#     loop.close()


# asyncio.create_task(load_media_async())


# Thread(target=load_media, daemon=True).start()
# Thread(target=asyncio.run, args=(load_media_async(),), daemon=True).start()


class LoadMedia(QThread):
    
    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:
            # print('sex')
            try:
                if message_with_media_to_load:
                    path_to_file, message = message_with_media_to_load.pop()
                    print(path_to_file)
                    client.download_media(message, path_to_file)
                    print('loaded')
                    # await asyncio.sleep(.3)

            except:
                create_exception_log()

