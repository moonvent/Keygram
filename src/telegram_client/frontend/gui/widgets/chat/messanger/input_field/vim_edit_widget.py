from enum import IntEnum
import functools
import re
from typing import Callable, Literal
from PySide6.QtCore import QEvent, QKeyCombination, QObject, Qt
from PySide6.QtGui import QFontDatabase, QKeyEvent, QKeySequence, QShortcut, QTextCursor
from src.database.keymaps import Keymaps
from src.services.database.models.keymaps import get_keybinds
from src.services.load_internalization import _
from PySide6.QtWidgets import QTextEdit
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts

from src.config import CURSOR_SIZE, FONT_SIZE, INPUT_FIELD_HEIGHT


class Keybinds:
    """
        Class for create keybinds list for vim editor
    """

    def get_binds_from_db(self, keymap: Keymaps) -> tuple[str, ...]:
        return get_keybinds(title=keymap)

    def pack_in_keysequence(self, binds: tuple[str, ...]) -> tuple[QKeySequence, ...]:
        return tuple(QKeySequence(bind) for bind in binds)

    def create_qt_bind(self, keymap: Keymaps) -> tuple[QKeySequence, ...]:
        binds = get_keybinds(title=keymap)
        return self.pack_in_keysequence(binds=binds)


class InsertType(IntEnum):
    StartOfString = 1
    CurrentSymbol = 2
    NextSymbol = 3
    EndOfString = 4


class VimWidget(QTextEdit,
                Keybinds):
    command_mode: bool = False
    visual_mode: bool = False
    insert_mode: bool = False

    binds_with_methods: dict[QKeySequence, Callable] = None         # dict, key - shortcut, value - method

    # start_selection_pos: int = None

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

    def set_writable_font(self):
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSizeF(FONT_SIZE)
        self.setFont(font)

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

                Keymaps.TO_VISUAL_MODE_IN_INSERT_FIELD: self.to_visual_in_insert_field,
                }

        self.binds_with_methods = {}

        for keymap, method in setup_keybinds_dict.items():
            for shortcut in self.create_qt_bind(keymap=keymap):
                self.binds_with_methods[shortcut] = method
            
    def send_message(self):
        self.parent().send_message()

    def handle_keybind(self, event: QKeyEvent) -> bool:
        """
            Handle pressed keybind, if need to ignore return True
        """
        pressed_key = QKeySequence(event.keyCombination())

        if pressed_key in self.binds_with_methods:
            return self.binds_with_methods[pressed_key]()

    def again_in_insert_mode(self,
                             to_position: InsertType = InsertType.CurrentSymbol):
        if self.command_mode:
            self.setReadOnly(False)
            self.switch_to_insert_mode()
            self.setCursorWidth(1)

            match to_position:
                case to_position.NextSymbol:
                    self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                            amount_sym=1)

                case to_position.StartOfString:
                    self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                            amount_sym=self.textCursor().position()
                                            )

                case to_position.EndOfString:
                    self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                            amount_sym=len(self.toPlainText()) - self.textCursor().position()
                                            )

            return True

    def switch_to_command_mode_from_insert(self):
        if self.visual_mode:
            self.clear_selection()
            self.switch_to_command_mode()

        elif self.insert_mode:
            self.setReadOnly(True)
            self.setCursorWidth(CURSOR_SIZE)
            self.setTextInteractionFlags(self.textInteractionFlags() | Qt.TextSelectableByKeyboard)
            self.switch_to_command_mode()

    def custom_move_cursor(self, 
                           direction: QTextCursor.MoveOperation, 
                           amount_sym: int):
        """
            Custom move cursor method for DRY
        """
        if not self.insert_mode:
            cursor = self.textCursor()
            cursor.movePosition(direction, 
                                QTextCursor.MoveMode.KeepAnchor if self.visual_mode else QTextCursor.MoveMode.MoveAnchor,
                                n=amount_sym,
                                )
            self.setTextCursor(cursor)

    def move_to_back_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[:self.textCursor().position()]
            amount_sym_to_left = len(re.search(r'(\b|\S)\w*\s*$', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                    amount_sym=amount_sym_to_left)


    def move_to_start_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[:self.textCursor().position()]
            amount_sym_to_left = len(re.search(r'[^\s]*\s*$', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                    amount_sym=amount_sym_to_left)

    def move_to_forward_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[self.textCursor().position():]
            amount_sym_to_left = len(re.search(r'^\s*\w*\b', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                    amount_sym=amount_sym_to_left)

    def move_to_end_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[self.textCursor().position():]
            amount_sym_to_left = len(re.search(r'^\s*\w*[^\s]*', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                    amount_sym=amount_sym_to_left)

    def to_visual_in_insert_field(self):
        self.switch_to_visual_mode()

    def clear_selection(self):
        c = self.textCursor()
        c.clearSelection()
        self.setTextCursor(c)
