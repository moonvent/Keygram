"""
    Dectibe dialog list widget
"""


import asyncio
from typing import List
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QPushButton, QScrollBar, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from telethon.tl.custom import dialog 
from telethon.tl.custom.dialog import Dialog as TTDialog
from telethon.tl.types import User
from src.database.keymaps import Keymaps
from src.services.database.models.keymaps import get_keybinds
from src.config import ACTIVE_DIALOG_NAME, AMOUNT_DIALOGS_BEFORE_SCROLLABLE_DIALOG, AMOUNT_DIALOGS_IN_HEIGHT, DIALOG_NAME, DIALOG_WIDGET_HEIGHT, MAIN_WIDGET_HEIGHT, DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget, _KeyboardShortcuts
from src.telegram_client.backend.dialogs.dialogs import get_dialogs
from src.telegram_client.frontend.gui.widgets.dialogs.dialog import Dialog
from src.telegram_client.frontend.gui.widgets.chat.chat import Chat


class DialogList(_CoreWidget, _KeyboardShortcuts):
    """
        Dialog list widget, with inner dialogs
    """
    telethon_dialogs: List[TTDialog] = []
    gui_dialogs: List[Dialog] = []
    _active_dialog: Dialog = None
    vertical_scroll: QScrollBar = None
    user: User = None

    index_to_continue_scroll_up: int = 1        # dialogs index which be ignored for scrolling
    index_to_continue_scroll_down: int = 8      # dialogs index which be ignored for scrolling

    _chat: Chat = None

    def __init__(self, parent, user) -> None:
        self.user = user
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.loaded_ui = True
        self.set_layout()
        self.load_dialogs_in_ui()
        self.set_keyboard_shortcuts()

    def load_dialogs_in_ui(self):
        self.load_dialogs_from_telegram()
        self.handle_dialogs()

    def load_dialogs_from_telegram(self):
        """
            Load dialogs from telethon
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_dialogs(dialogs_list=self.telethon_dialogs))

    def handle_dialogs(self):
        for dialog_number, tt_dialog in enumerate(self.telethon_dialogs):
            gui_dialog = Dialog(self, 
                                tt_dialog, 
                                current_dialog_status=not dialog_number,
                                user=self.user)

            if gui_dialog.active_dialog:
                self.active_dialog = gui_dialog

            self.gui_dialogs.append(gui_dialog)

            self.layout().addWidget(gui_dialog)

    @property
    def chat(self):
        return self._chat

    @chat.setter
    def chat(self, chat):
        self._chat = chat
        if not self._chat.dialog:
            self.chat.dialog = self.active_dialog.dialog

    @property
    def active_dialog(self):
        return self._active_dialog

    @active_dialog.setter
    def active_dialog(self, gui_dialog: Dialog):
        self._active_dialog = gui_dialog
        if self.chat:
            self.chat.dialog = gui_dialog.dialog

    def set_keyboard_shortcuts(self):
        self.set_keybind_handlers(keybind_title=Keymaps.DOWN_IN_DIALOGS_LIST,
                                  method=self.activate_chat_below)

        self.set_keybind_handlers(keybind_title=Keymaps.UP_IN_DIALOGS_LIST,
                                  method=self.activate_chat_above)

    def activate_chat_above(self):
        self.active_dialog.setObjectName(DIALOG_NAME)
        active_dialog_index = self.gui_dialogs.index(self.active_dialog)

        if active_dialog_index == 0:        # for infine scroll
            return
            # self.active_dialog = self.gui_dialogs[-1]
            # self.vertical_scroll.setValue(self.vertical_scroll.maximum())

        else:
            self.active_dialog = self.gui_dialogs[active_dialog_index - 1]

        self.active_dialog.setObjectName(ACTIVE_DIALOG_NAME)
        self.load_styles()

        if active_dialog_index <= self.index_to_continue_scroll_up:
            self.vertical_scroll.setValue(self.vertical_scroll.value() - DIALOG_WIDGET_HEIGHT)
            if active_dialog_index != 1:
                self.index_to_continue_scroll_up -= 1
                self.index_to_continue_scroll_down -= 1
        
    def activate_chat_below(self):
        self.active_dialog.setObjectName(DIALOG_NAME)
        active_dialog_index = self.gui_dialogs.index(self.active_dialog)

        if active_dialog_index == len(self.gui_dialogs) - 1:        # for infine scroll
            return
            # # in code about happend smth straight
            # self.active_dialog = self.gui_dialogs[0]
            # print('before', self.vertical_scroll.value())
            # print('minimum', self.vertical_scroll.minimum())
            # while self.vertical_scroll.value():
                # self.vertical_scroll.setValue(self.vertical_scroll.value() - DIALOG_WIDGET_HEIGHT)
            # print('after', self.vertical_scroll.value())
        else:
            self.active_dialog = self.gui_dialogs[active_dialog_index + 1]

        self.active_dialog.setObjectName(ACTIVE_DIALOG_NAME)
        self.load_styles()        
         
        if active_dialog_index >= self.index_to_continue_scroll_down:
            self.vertical_scroll.setValue(self.vertical_scroll.value() + DIALOG_WIDGET_HEIGHT)
            if (len(self.gui_dialogs) - 2) != active_dialog_index:
                self.index_to_continue_scroll_down += 1
                self.index_to_continue_scroll_up += 1

