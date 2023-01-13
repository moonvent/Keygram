from enum import IntEnum
from src.services.logging.setup_logger import logger


logger.info('Create a internalization of about every bind')


class Keymaps(IntEnum):
    DOWN_IN_DIALOGS_LIST = 1
    UP_IN_DIALOGS_LIST = 2

    TO_LEFT_PAN = 3
    TO_RIGHT_PAN = 4
    TO_UP_PAN = 5
    TO_DOWN_PAN = 6

    DOWN_IN_MESSANGER_LIST = 7
    UP_IN_MESSANGER_LIST = 8

    BACK_OF_WORD = 9
    START_OF_WORD = 10

    FORWARD_OF_WORD = 11
    END_OF_WORD = 12

    LEFT_ON_SYM = 13
    DOWN_ON_STRING = 14
    UP_ON_STRING = 15
    RIGHT_ON_SYM = 16

    INSERT_IN_CURRENT_SYM = 17
    INSERT_IN_NEXT_SYM = 18
    INSERT_IN_START = 19
    INSERT_IN_END = 20

    ESCAPE = 21
    RETURN = 22

    TO_VISUAL_MODE_IN_INSERT_FIELD = 23

    CUT_SELECTED = 24
    REMOVE_ONE_SYM = 25

    COPY_SELECTED = 26

    PASTE_AFTER = 27
    PASTE_BEFORE = 28

    END_OF_STRING = 29
    START_OF_STRING = 30

    INSERT_MODE_IN_INPUT_FIELD = 31

