from telethon.helpers import TotalList
from telethon.tl.patched import Message
from src.config import AMOUNT_MESSAGE_LIMIT
from src.telegram_client.backend.client_init import client


async def get_messages(chat_id: int, offset: int = 0) -> TotalList[Message]:
    return await client.get_messages(chat_id, AMOUNT_MESSAGE_LIMIT)

