import os
from os.path import isdir
from src.config import STYLES_FOLDER_PATH
from src.services.logging.setup_logger import logger


def read_files(path: str) -> str:
    """
        Recursive function for read all styles file
    """
    styles = ''

    for file in os.listdir(path):
        current_file = os.path.join(path, file)

        if isdir(current_file):
            styles += read_files(current_file)

        else:
            with open(current_file, 'r') as style_file:
                styles += style_file.read() + '\n' 

    return styles

def load_all_styles_file() -> str:
    """
        Load all file with styles
        :WARNING: all ids of elements MUST BE UNIQ
        :return str: all styles in one string
    """
    # logger.critical('Add check uniq id')
    return read_files(STYLES_FOLDER_PATH).replace('\n', '')

