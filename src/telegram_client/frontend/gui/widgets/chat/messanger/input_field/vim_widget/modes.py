from src.config import CURSOR_SIZE
from PySide6.QtCore import Qt


class VimModes:
    """
        Work with modes in vim
    """
    command_mode: bool = False
    visual_mode: bool = False
    insert_mode: bool = False

    def switch_to_insert_mode(self):
        self.insert_mode = True
        self.command_mode = False
        self.visual_mode = False

    def switch_to_command_mode(self):
        self.insert_mode = False
        self.command_mode = True
        self.visual_mode = False

    def switch_to_visual_mode(self):
        self.insert_mode = False
        self.command_mode = False
        self.visual_mode = True

    def switch_to_command_mode_from_insert(self):
        """
            Switch to insert mode from other mods and setup a few features
        """

        if self.visual_mode:
            self.clear_selection()
            self.switch_to_command_mode()

        elif self.insert_mode:
            self.setReadOnly(True)
            self.setCursorWidth(CURSOR_SIZE)
            self.setTextInteractionFlags(self.textInteractionFlags() | Qt.TextSelectableByKeyboard)
            self.switch_to_command_mode()
            self.make_cursor_visible()

    def switch_before_change_pan(self):
        self.setReadOnly(True)
        self.switch_to_command_mode()

    def make_cursor_visible(self):
        """
            Make cursor visible after entry in command mode from other modes
        """
        self.setTextCursor(self.textCursor())
