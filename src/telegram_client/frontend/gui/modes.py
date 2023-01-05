"""
    Describe mode service
"""
from src.services.logging.setup_logger import logger


class Modes:
    visual_mode: bool = True
    insert_mode: bool = True

    command_mode: bool = True

    def switch_to_command_mode(self):
        logger.debug('Switch to command mode')
        self.visual_mode = False
        self.command_mode = True
        self.insert_mode = False

    def switch_to_visual_mode(self):
        logger.debug('Switch to visual mode')
        self.visual_mode = True
        self.command_mode = False
        self.insert_mode = False

    def switch_to_insert_mode(self):
        logger.debug('Switch to insert mode')
        self.visual_mode = False
        self.command_mode = False
        self.insert_mode = True

