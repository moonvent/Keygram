"""
    Describe dialog list widget
"""


import asyncio
from typing import List
from PySide6.QtGui import QColor, QKeySequence, QPalette, QShortcut
from PySide6.QtWidgets import QPushButton, QScrollBar, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from telethon.tl.custom import dialog 
from telethon.tl.custom.dialog import Dialog as TTDialog
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.database.keymaps import Keymaps
from src.services.database.models.keymaps import get_keybinds
from src.config import ACTIVE_DIALOG_NAME, AMOUNT_DIALOGS_BEFORE_SCROLLABLE_DIALOG, AMOUNT_DIALOGS_IN_HEIGHT, DIALOG_ACTIVE_NAME, DIALOG_NAME, DIALOG_WIDGET_HEIGHT, MAIN_WIDGET_HEIGHT, DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts
from src.telegram_client.backend.dialogs.dialogs import get_dialogs
from src.telegram_client.frontend.gui.widgets.dialogs.dialog import Dialog
from src.telegram_client.frontend.gui.widgets.chat.chat import Chat
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.keyboard import DialogListKeyboard


class DialogList(_CoreWidget, 
                 DialogListKeyboard):
    """
        Dialog list widget, with inner dialogs
    """
    telethon_dialogs: List[TTDialog] = None
    gui_dialogs: List[Dialog] = []
    _active_dialog: Dialog = None
    vertical_scroll: QScrollBar = None
    user: User = None

    index_to_continue_scroll_up: int = 1        # dialogs index which be ignored for scrolling
    index_to_continue_scroll_down: int = 8      # dialogs index which be ignored for scrolling

    gui_dialogs_with_id: dict[int, TTDialog] = {}

    _chat: Chat = None

    main_window: QWidget = None

    def __init__(self, parent, user) -> None:
        self.user = user
        self.active_pan = True
        self.main_window = parent
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setObjectName(DIALOG_ACTIVE_NAME)
        self.load_dialogs_in_ui()
        self.set_keyboard_shortcuts()

        client.dialog_update_handler = self.dialog_update_handler

    def dialog_update_handler(self, dialog, message: Message, dialog_id: int):
        if gui_dialog := self.gui_dialogs_with_id.get(dialog_id):
            gui_dialog.update_data(message=message)

    def load_dialogs_in_ui(self):
        self.load_dialogs_from_telegram()
        self.handle_dialogs()

    def load_dialogs_from_telegram(self):
        """
            Load dialogs from telethon
        """
        self.telethon_dialogs = get_dialogs()

    def handle_dialogs(self):
        for dialog_number, tt_dialog in enumerate(self.telethon_dialogs):
            gui_dialog = Dialog(self, 
                                tt_dialog, 
                                current_dialog_status=not dialog_number,
                                user=self.user)

            if gui_dialog.active_dialog:
                self.active_dialog = gui_dialog

            self.gui_dialogs.append(gui_dialog)
            self.gui_dialogs_with_id[tt_dialog.id] = gui_dialog

            self.layout().addWidget(gui_dialog)

    @property
    def chat(self):
        return self._chat

    @chat.setter
    def chat(self, chat):
        self._chat = chat
        # if not self._chat.dialog:
        self.chat.dialog = self.active_dialog.dialog

    @property
    def active_dialog(self):
        return self._active_dialog

    @active_dialog.setter
    def active_dialog(self, gui_dialog: Dialog):
        self._active_dialog = gui_dialog
        gui_dialog.clear_unread_status()
        if self.chat:
            self.chat.dialog = gui_dialog.dialog

