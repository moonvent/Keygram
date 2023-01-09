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

    # def __init__(self) -> None:
    #     self.load_vim_keybinds()

    def get_binds_from_db(self, keymap: Keymaps) -> tuple[str, ...]:
        return get_keybinds(title=keymap)

    def pack_in_keysequence(self, binds: tuple[str, ...]) -> tuple[QKeySequence, ...]:
        return tuple(QKeySequence(bind) for bind in binds)

    def create_qt_bind(self, keymap: Keymaps) -> tuple[QKeySequence, ...]:
        binds = get_keybinds(title=keymap)
        return self.pack_in_keysequence(binds=binds)

    # def load_vim_keybinds(self):
    #     self.BACK_OF_WORD = self.create_qt_bind(keymap=Keymaps.BACK_OF_WORD)
    #     self.START_OF_WORD = self.create_qt_bind(keymap=Keymaps.START_OF_WORD)
    #
    #     self.FORWARD_OF_WORD = self.create_qt_bind(keymap=Keymaps.FORWARD_OF_WORD)
    #     self.END_OF_WORD = self.create_qt_bind(keymap=Keymaps.END_OF_WORD)
    #
    #     self.LEFT_ON_SYM = self.create_qt_bind(keymap=Keymaps.LEFT_ON_SYM)
    #     self.RIGHT_ON_SYM = self.create_qt_bind(keymap=Keymaps.RIGHT_ON_SYM)
    #     self.UP_ON_STRING = self.create_qt_bind(keymap=Keymaps.UP_ON_STRING)
    #     self.DOWN_ON_STRING = self.create_qt_bind(keymap=Keymaps.DOWN_ON_STRING)
    #
    #     self.INSERT_IN_CURRENT_SYM = self.create_qt_bind(keymap=Keymaps.INSERT_IN_CURRENT_SYM)
    #     self.INSERT_IN_NEXT_SYM = self.create_qt_bind(keymap=Keymaps.INSERT_IN_NEXT_SYM)
    #     self.INSERT_IN_START = self.create_qt_bind(keymap=Keymaps.INSERT_IN_START)
    #     self.INSERT_IN_END = self.create_qt_bind(keymap=Keymaps.INSERT_IN_END)


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

    def eventFilter(self, 
                    watched: QObject, 
                    event: QEvent) -> bool:

        if self.hasFocus() and event.type() == QEvent.KeyPress:
            if self.handle_keybind(event=event):
                return True
            
        return super().eventFilter(watched, event)

    def setup_keybind(self):
        setup_keybinds_dict = {
                # Keymaps.RETURN: self.send_message,
                # Keymaps.ESCAPE: self.switch_to_command_mode_from_insert,

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

        match pressed_key:
            case Qt.Key_Escape:
                self.switch_to_command_mode_from_insert()
            case Qt.Key_Return:
                self.send_message()
            case _:
                if self.command_mode:
                    return self.binds_with_methods[pressed_key]()

        # match pressed_key:
        #     case Qt.Key_Return:
        #         self.parent().send_message()
        #
        #     case Qt.Key_Escape:
        #         self.switch_to_command_mode_from_insert()
        #
        #     case keybind if keybind in self.keybinds.BACK_OF_WORD and self.command_mode:
        #         self.move_to_back_of_word()
        #         
        #     case keybind if keybind in self.keybinds.START_OF_WORD and self.command_mode:
        #         self.move_to_start_of_word()
        #
        #     case keybind if keybind in self.keybinds.FORWARD_OF_WORD and self.command_mode:
        #         self.move_to_forward_of_word()
        #         
        #     case keybind if keybind in self.keybinds.END_OF_WORD and self.command_mode:
        #         self.move_to_end_of_word()
        #
        #     case keybind if keybind in self.keybinds.LEFT_ON_SYM and self.command_mode:
        #         self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
        #                                 amount_sym=1)
        #         
        #     case keybind if keybind in self.keybinds.RIGHT_ON_SYM and self.command_mode:
        #         self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
        #                                 amount_sym=1)
        #
        #     case keybind if keybind in self.keybinds.UP_ON_STRING and self.command_mode:
        #         self.custom_move_cursor(direction=QTextCursor.MoveOperation.Up,
        #                                 amount_sym=1)
        #         
        #     case keybind if keybind in self.keybinds.DOWN_ON_STRING and self.command_mode:
        #         self.custom_move_cursor(direction=QTextCursor.MoveOperation.Down,
        #                                 amount_sym=1)
        #
        #     case keybind if keybind in self.keybinds.INSERT_IN_START and self.command_mode:
        #         self.again_in_insert_mode(to_position=InsertType.StartOfString)
        #         return True         # signal for not print I
        #
        #     case keybind if keybind in self.keybinds.INSERT_IN_CURRENT_SYM and self.command_mode:
        #         self.again_in_insert_mode(to_position=InsertType.CurrentSymbol)
        #         return True         # signal for not print I
        #
        #     case keybind if keybind in self.keybinds.INSERT_IN_END and self.command_mode:
        #         self.again_in_insert_mode(to_position=InsertType.EndOfString)
        #         return True         # signal for not print I
        #
        #     case keybind if keybind in self.keybinds.INSERT_IN_NEXT_SYM and self.command_mode:
        #         self.again_in_insert_mode(to_position=InsertType.NextSymbol)
        #         return True         # signal for not print I
        #         
        #     case _:
        #         ...

    def again_in_insert_mode(self,
                             to_position: InsertType = InsertType.CurrentSymbol):
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
        cursor = self.textCursor()
        cursor.movePosition(direction, 
                            n=amount_sym)
        self.setTextCursor(cursor)

    def move_to_back_of_word(self):
        text = self.toPlainText()[:self.textCursor().position()]
        amount_sym_to_left = len(re.search(r'(\b|\S)\w*\s*$', text).group())

        self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                amount_sym=amount_sym_to_left)


    def move_to_start_of_word(self):
        text = self.toPlainText()[:self.textCursor().position()]
        amount_sym_to_left = len(re.search(r'\w*\s*$', text).group())

        self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                amount_sym=amount_sym_to_left)

    def move_to_forward_of_word(self):
        text = self.toPlainText()[self.textCursor().position():]
        amount_sym_to_left = len(re.search(r'^\s*\w*\b', text).group())

        self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                amount_sym=amount_sym_to_left)

    def move_to_end_of_word(self):
        text = self.toPlainText()[self.textCursor().position():]
        amount_sym_to_left = len(re.search(r'^\s*\w*[^\s]*', text).group())

        self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                amount_sym=amount_sym_to_left)

