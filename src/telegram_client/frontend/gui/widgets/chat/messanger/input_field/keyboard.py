from src.database.keymaps import Keymaps
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts


class InputFieldKeyboard(_KeyboardShortcuts):

    def set_keyboard_shortcuts(self):
        super().set_widget_shortcuts()

        self.set_keybind_handlers(keybind_title=Keymaps.INSERT_MODE_IN_INPUT_FIELD,
                                  method=self.activate)

        # self.set_keybind_handlers(keybind_title=Keymaps.UP_IN_DIALOGS_LIST,
        #                           method=self.activate_message_above)

    # def active_vim_editor(self):
    #     self.activate()
    #

