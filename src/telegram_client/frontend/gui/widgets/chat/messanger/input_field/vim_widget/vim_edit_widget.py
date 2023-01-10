from enum import IntEnum
import functools
import re
from typing import Callable, Literal
from PySide6.QtCore import QEvent, QKeyCombination, QObject, Qt
from PySide6.QtGui import QFontDatabase, QKeyEvent, QKeySequence, QShortcut, QTabletEvent, QTextCursor
from src.database.keymaps import Keymaps
from src.services.database.models.keymaps import get_keybinds
from src.services.load_internalization import _
from PySide6.QtWidgets import QTextEdit
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts

from src.config import CURSOR_SIZE, FONT_SIZE, INPUT_FIELD_HEIGHT
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.navigation import VimNavigation
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.clipboard import VimClipboard
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.keybinds import VimKeybinds
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.insert import VimInsert
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.modes import VimModes
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.insert import InsertType
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.selecting import VimSelection


class VimWidget(QTextEdit,
                VimModes,
                VimKeybinds,
                VimInsert,
                VimNavigation,
                VimClipboard,
                VimSelection):

    def __init__(self, parent):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setPlaceholderText(_('write_message'))
        self.setObjectName('input_field')
        self.setFixedHeight(INPUT_FIELD_HEIGHT)
        self.installEventFilter(self)
        self.set_writable_font()
        self.setup_keybind()
        # self.set_keyboard_shortcuts() # doesn't work here

    def text(self):
        """
            For more understandable coding
        """
        return self.toPlainText()

    def send_message(self):
        self.parent().send_message()

    def set_writable_font(self):
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSizeF(FONT_SIZE)
        self.setFont(font)

    def eventFilter(self, 
                    watched: QObject, 
                    event: QEvent) -> bool:

        if self.hasFocus() and event.type() == QEvent.KeyPress:
            if self.handle_keybind(event=event):
                return True
            
        return super().eventFilter(watched, event)

    def setup_keybind(self):
        setup_keybinds_dict = {
                Keymaps.RETURN: self.send_message,
                Keymaps.ESCAPE: self.switch_to_command_mode_from_insert,

                Keymaps.BACK_OF_WORD: self.move_to_back_of_word,
                Keymaps.START_OF_WORD: self.move_to_start_of_word,

                Keymaps.FORWARD_OF_WORD: self.move_to_forward_of_word,
                Keymaps.END_OF_WORD: self.move_to_end_of_word,

                Keymaps.LEFT_ON_SYM: functools.partial(self.custom_move_cursor, QTextCursor.MoveOperation.Left, 1),
                Keymaps.RIGHT_ON_SYM: functools.partial(self.custom_move_cursor, QTextCursor.MoveOperation.Right, 1),
                Keymaps.UP_ON_STRING: functools.partial(self.custom_move_cursor, QTextCursor.MoveOperation.Up, 1),
                Keymaps.DOWN_ON_STRING: functools.partial(self.custom_move_cursor, QTextCursor.MoveOperation.Down, 1),

                Keymaps.INSERT_IN_CURRENT_SYM: functools.partial(self.again_in_insert_mode, InsertType.CurrentSymbol),
                Keymaps.INSERT_IN_NEXT_SYM: functools.partial(self.again_in_insert_mode, InsertType.NextSymbol),
                Keymaps.INSERT_IN_START: functools.partial(self.again_in_insert_mode, InsertType.StartOfString),
                Keymaps.INSERT_IN_END: functools.partial(self.again_in_insert_mode, InsertType.EndOfString),

                Keymaps.TO_VISUAL_MODE_IN_INSERT_FIELD: self.switch_to_visual_mode,

                Keymaps.CUT_SELECTED: self.cut_selected,
                Keymaps.COPY_SELECTED: self.copy_selected,
                Keymaps.REMOVE_ONE_SYM: self.remove_one_sym,
                Keymaps.PASTE_AFTER: self.paste_data_after_sym,
                Keymaps.PASTE_BEFORE: self.paste_data_before_sym,
                }

        self.binds_with_methods = {}

        for keymap, method in setup_keybinds_dict.items():
            for shortcut in self.create_qt_bind(keymap=keymap):
                self.binds_with_methods[shortcut] = method
            
