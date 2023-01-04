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

