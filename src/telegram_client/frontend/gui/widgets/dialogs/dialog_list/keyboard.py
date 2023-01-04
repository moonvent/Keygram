from PySide6.QtWidgets import QWidget
from src.config import ACTIVE_DIALOG_NAME, DIALOG_NAME, DIALOG_WIDGET_HEIGHT
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts
from src.database.keymaps import Keymaps


class DialogListKeyboard(_KeyboardShortcuts):

    def set_keyboard_shortcuts(self):
        super().set_widget_shortcuts()

        self.set_keybind_handlers(keybind_title=Keymaps.DOWN_IN_DIALOGS_LIST,
                                  method=self.activate_chat_below)

        self.set_keybind_handlers(keybind_title=Keymaps.UP_IN_DIALOGS_LIST,
                                  method=self.activate_chat_above)

    def switch_dialog(func):
        """
            Change dialog style and reload it
        """

        def wrapped(self, *args, **kwargs):

            self.active_dialog.setObjectName(DIALOG_NAME)

            func(self, *args, **kwargs)

            self.active_dialog.setObjectName(ACTIVE_DIALOG_NAME)
            self.load_styles()

        return wrapped

    @switch_dialog
    def activate_chat_above(self):
        active_dialog_index = self.gui_dialogs.index(self.active_dialog)

        if active_dialog_index == 0:        # for infine scroll
            return

        else:
            self.active_dialog = self.gui_dialogs[active_dialog_index - 1]

        if active_dialog_index <= self.index_to_continue_scroll_up:
            self.vertical_scroll.setValue(self.vertical_scroll.value() - DIALOG_WIDGET_HEIGHT)
            if active_dialog_index != 1:
                self.index_to_continue_scroll_up -= 1
                self.index_to_continue_scroll_down -= 1
        
    @switch_dialog
    def activate_chat_below(self):
        active_dialog_index = self.gui_dialogs.index(self.active_dialog)

        if active_dialog_index == len(self.gui_dialogs) - 1:        # for infine scroll
            return
            
        else:
            self.active_dialog = self.gui_dialogs[active_dialog_index + 1]

        if active_dialog_index >= self.index_to_continue_scroll_down:
            self.vertical_scroll.setValue(self.vertical_scroll.value() + DIALOG_WIDGET_HEIGHT)
            if (len(self.gui_dialogs) - 2) != active_dialog_index:
                self.index_to_continue_scroll_down += 1
                self.index_to_continue_scroll_up += 1

