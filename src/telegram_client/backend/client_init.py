"""
    Client initialization
"""

import os
from src.services import load_env_vars              # for load env vars from .env file
from telethon import TelegramClient, events, sync


api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']

client = TelegramClient('session_name', api_id, api_hash)
client.start()


async def get_me():
    """
        Get user object, for future needs
    """
    return await client.get_me()


# with client:
#     client.run_until_disconnected()

# client.send_message('moonvent', 'Hello! Talking to you from Telethon')

#tclient.send_file('username', '/home/myself/Pictures/holidays.jpg')

# client.download_profile_photo('me')
# messages = client.get_messages('username')
# messages[0].download_media()
#
# @client.on(events.NewMessage(pattern='(?i)hi|hello'))
# async def handler(event):
#     await event.respond('Hey!')
