from src.database.keymaps import Keymaps
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts


class InputFieldKeyboard(_KeyboardShortcuts):

    def set_keyboard_shortcuts(self):
        super().set_widget_shortcuts()

