import os

from src.config import APP_NAME_WITHOUT_SPACES, LOCALE_FOLDER_PATH
from src.services.logging.setup_logger import logger


def update_langs():
    """
        Recompile all language translations
    """
    app_name = APP_NAME_WITHOUT_SPACES
    logger.critical('You MUST start this command from root project directory')
    for lang in os.listdir(LOCALE_FOLDER_PATH):
        logger.info(f'Recompile {lang}')
        command = f'msgfmt src/locale/{lang}/LC_MESSAGES/{app_name}.po -o src/locale/{lang}/LC_MESSAGES/{app_name}.mo'
        os.system(command)
        logger.info(f'Recompile {lang} Complete.')

