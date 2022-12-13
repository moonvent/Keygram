"""
    General config file
"""


import os


def check_exists_folder(path: str):
    """
        Check exists every folder
    """
    if not os.path.exists(path):
        create_folder(path)


def create_folder(path: str):
    """
        Create not exists folder
    """
    os.mkdir(path)


SOURCE_FOLDER_NAME = 'src'

STATIC_FOLDER_NAME = 'static'
STATIC_FOLDER_PATH = os.path.join(SOURCE_FOLDER_NAME, STATIC_FOLDER_NAME)

check_exists_folder(path=STATIC_FOLDER_PATH)

AVATARS_FOLDER_NAME = 'avatars'
AVATARS_FOLDER_PATH = os.path.join(STATIC_FOLDER_PATH, AVATARS_FOLDER_NAME)

check_exists_folder(path=AVATARS_FOLDER_PATH)


