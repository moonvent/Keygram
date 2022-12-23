"""
    General config file
"""


import os


"""
    Work with folders
"""


def check_exists_folder(path: str,
                        error: bool = False):
    """
        Check exists every folder
        :param path: path which need check
        :param error: if true, raise DirectoryNotFoundError, cause this directore need to work
    """
    if not os.path.exists(path):
        if error:
            raise FileNotFoundError(f'Directory {path} not found, please solve this before start the app')
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

LOCALE_FOLDER_NAME = 'locale'
LOCALE_FOLDER_PATH = os.path.join(SOURCE_FOLDER_NAME, LOCALE_FOLDER_NAME)

check_exists_folder(path=LOCALE_FOLDER_PATH, 
                    error=True)
STYLES_FOLDER_NAME = 'styles'
STYLES_FOLDER_PATH = os.path.join(STATIC_FOLDER_PATH, STYLES_FOLDER_NAME)

check_exists_folder(path=STYLES_FOLDER_PATH, 
                    error=True)

"""
    Work with constants
"""


APP_NAME_WITH_SPACES = 'Keygram'
APP_NAME_WITHOUT_SPACES = 'Keygram'

MAIN_WIDGET_WIDTH = 1920
MAIN_WIDGET_HEIGHT = 1080

#
# Work with dialogs constants
#

AMOUNT_DIALOGS_IN_HEIGHT = 10
AMOUNT_DIALOGS_IN_WIDTH = 25

AMOUNT_DIALOGS_BEFORE_SCROLLABLE_DIALOG = 1 + 2     # first component it's how much dialog be until border

DIALOG_WIDGET_HEIGHT = int(MAIN_WIDGET_HEIGHT / 100 * AMOUNT_DIALOGS_IN_HEIGHT)
DIALOG_WIDGET_WIDTH = int(MAIN_WIDGET_WIDTH / 100 * AMOUNT_DIALOGS_IN_WIDTH)

DIALOGS_LOAD_LIMIT = 20

AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT = 50
AMOUNT_SYMBOLS_FOR_CUTTING_TITLE = 30

AVATAR_HEIGHT_IN_DIALOG = 75
AVATAR_WEIGHT_IN_DIALOG = 75

LENGTH_TITLE = int(MAIN_WIDGET_WIDTH / 100 * 25)

DIALOG_SCROLL_WIDTH = 16

DIALOG_NAME = 'dialog'
ACTIVE_DIALOG_NAME = 'dialog_active'

"""
    Work with info menu
"""

INFO_MENU_AVATAR_SIZE = 70
INFO_MENU_HEIGHT = DIALOG_WIDGET_HEIGHT


"""
    Work with db
"""

DB_NAME = 'sqlite:///db.db'

KEYMAPS_TABLE = 'keymaps'
GLOBAL_DATA_TABLE = 'global_data'
KEYBINDS_TABLE = 'keybinds'

# All keymaps consts exists in src/database/keymaps.py


"""
    Messanger info
"""

AMOUNT_MESSAGE_LIMIT = 30

MESSAGE_NAME = 'message'

MESSAGES_FONT_SIZE = 15

FONT_NAME = 'Helvetica'

"""
    Input field
"""

INPUT_FIELD_HEIGHT = 60
