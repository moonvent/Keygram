import asyncio
from typing import List
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from telethon.tl.custom.dialog import Dialog as TTDialog
from src.config import ACTIVE_DIALOG_NAME, DIALOG_NAME, MAIN_WIDGET_HEIGHT, DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget, _KeyboardShortcuts
from src.telegram_client.backend.dialogs.dialogs import get_dialogs
from src.telegram_client.frontend.gui.widgets.dialogs.dialog import Dialog


class DialogList(_CoreWidget, _KeyboardShortcuts):
    """
        Dialog list widget, with inner dialogs
    """
    telethon_dialogs: List[TTDialog] = []
    gui_dialogs: List[Dialog] = []
    active_dialog: Dialog = None

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.load_dialogs_in_ui()
        self.set_keyboard_shortcuts()

    def load_dialogs_in_ui(self):
        # self.setStyleSheet('background-color: green')
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
                                current_dialog_status=not dialog_number)

            if gui_dialog.active_dialog:
                self.active_dialog = gui_dialog

            self.gui_dialogs.append(gui_dialog)

            self.layout().addWidget(gui_dialog)

    def set_keyboard_shortcuts(self):
        shortcut_down = QShortcut(QKeySequence('j'), self)
        shortcut_down.activated.connect(self.activate_chat_below)

        shortcut_down = QShortcut(QKeySequence('k'), self)
        shortcut_down.activated.connect(self.activate_chat_above)

    def activate_chat_above(self):
        self.active_dialog.setObjectName(DIALOG_NAME)
        active_dialog_index = self.gui_dialogs.index(self.active_dialog)
        self.active_dialog = self.gui_dialogs[active_dialog_index - 1]
        self.active_dialog.setObjectName(ACTIVE_DIALOG_NAME)
        self.load_styles()

    def activate_chat_below(self):
        self.active_dialog.setObjectName(DIALOG_NAME)
        active_dialog_index = self.gui_dialogs.index(self.active_dialog)
        self.active_dialog = self.gui_dialogs[active_dialog_index + 1]
        self.active_dialog.setObjectName(ACTIVE_DIALOG_NAME)
        self.load_styles()

