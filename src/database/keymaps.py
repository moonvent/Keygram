from enum import IntEnum
from src.services.logging.setup_logger import logger


logger.info('Create a internalization of about every bind')


class Keymaps(IntEnum):
    DOWN_IN_DIALOGS_LIST = 1
    UP_IN_DIALOGS_LIST = 2

