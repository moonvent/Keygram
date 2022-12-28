import os
from src.config import AVATARS_FOLDER_PATH
from src.telegram_client.backend.client_init import client
from telethon.hints import TotalList


def get_avatar_name(profile_id: int) -> str:
    """
        Generate name for avatar file
    """
    return os.path.join(AVATARS_FOLDER_PATH, f'{profile_id}.jpg')


def check_exists_avatar(avatar_path: str) -> bool:
    """
        Check exists avatar in avatar folders or not
    """
    return os.path.exists(avatar_path)


def download_avatars(dialogs: TotalList):
    """
        Download avatars for fast access in future
    """
    for dialog in dialogs:
        avatar_path = get_avatar_name(profile_id=dialog.id)
        if not check_exists_avatar(avatar_path=avatar_path):
            client.download_profile_photo(dialog.id,
                                          avatar_path)

