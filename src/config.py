"""
    General config file
"""


from enum import Enum
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

VIDEO_MESSAGE_NAME = 'video_messages'
VIDEO_MESSAGE_PATH = os.path.join(STATIC_FOLDER_PATH, VIDEO_MESSAGE_NAME)

check_exists_folder(path=VIDEO_MESSAGE_PATH)

# VOICE_FROM_VIDEO_NAME = 'temp_voices_from_videos'
# VOICE_FROM_VIDEO_NAME_PATH = os.path.join(VIDEO_MESSAGE_PATH, VOICE_FROM_VIDEO_NAME)
#
# check_exists_folder(path=VOICE_FROM_VIDEO_NAME_PATH)


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


BRIGHTNESS_NOT_ACTIVE_COEF = .2

APP_NAME_WITH_SPACES = 'Keygram'
APP_NAME_WITHOUT_SPACES = 'Keygram'

MAIN_WIDGET_WIDTH = 1920
MAIN_WIDGET_HEIGHT = 1080

#
# Work with dialogs constants
#


DIALOG_ACTIVE_NAME = 'dialog_list__active'
DIALOG_NOT_ACTIVE_NAME = 'dialog_list__not_active'


DIALOG_FONT_SIZE_TEXT = 15
DIALOG_FONT_SIZE_TITLE = 15

AMOUNT_DIALOGS_IN_HEIGHT = 10
AMOUNT_DIALOGS_IN_WIDTH = 25

AMOUNT_UNREAD_MARK = 30

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

INFO_MENU_AVATAR_SIZE = 50
INFO_MENU_HEIGHT = 60


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

SELECTED_MESSANGE_CSS_CLASS = 'selected_message'
NOT_SELECTED_MESSANGE_CSS_CLASS = 'not_selected_message'

"""
    Media viewer widget
"""

MEDIA_VIEWER_WIDGET_WIDTH = int(MAIN_WIDGET_WIDTH / 4.5)

VIDEO_MESSAGE_SIZE = 384
VIDEO_MESSAGE_THUMB_SIZE = 320

VIDEO_OUTPUT_HEIGHT = 426
VIDEO_OUTPUT_WIDTH = 240

INTERVAL_TO_CHANGE_POSITION = 1

"""
    Input field
"""

INPUT_FIELD_HEIGHT = 60

FONT_SIZE = 20
# CURSOR_SIZE = int(FONT_SIZE / 2)
CURSOR_SIZE = 12


"""
    Primary settings
"""

class SettingsEnum(Enum):
    SPEED = 'speed'
    VOLUME = 'volume'

PRIMARY_SETTINGS = {SettingsEnum.SPEED.value: 1,
                    SettingsEnum.VOLUME.value: 50}


CHAT_WIDTH = MAIN_WIDGET_WIDTH - MEDIA_VIEWER_WIDGET_WIDTH - DIALOG_WIDGET_WIDTH

CHAT_COLUMN_WIDTH = int(CHAT_WIDTH / 2.3)


"""
    Speed spinbox
"""

SPEED_STEP = .25

SPEED_SPINBOX_MAX = 10
SPEED_SPINBOX_MIN = 0 + SPEED_STEP


"""
    Volume slider
"""

VOLUME_SLIDER_MAX = 100
VOLUME_SLIDER_MIN = 0

VOLUME_STEP = 5


"""
    Photo message
"""


ADDITIONAL_PHOTO_WIDTH = 180
ADDITIONAL_PHOTO_HEIGHT = 90

