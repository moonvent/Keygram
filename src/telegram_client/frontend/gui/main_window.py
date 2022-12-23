import asyncio
from PySide6.QtWidgets import QHBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from telethon.tl.types import User
from src.services.frontend.load_all_styles import load_all_styles_file
from src.config import DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT, MAIN_WIDGET_WIDTH, STYLES_FOLDER_PATH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.scrollable_dialog_list import ScrollableDialogList
from src.telegram_client.backend.client_init import get_me
from src.telegram_client.frontend.gui.widgets.chat.chat import Chat


class MainWindow(_CoreWidget):
    """
        Main Window gui widget
    """
    dialogs_list: QWidget = None
    chat: Chat = None
    user: User = None
    
    def load_ui(self):
        self.set_fixed_size(MAIN_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT)
        self.set_layout()
        self.load_me()

        self.load_dialogs_list()
        self.load_chat_widget()

        self.load_styles()

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_dialogs_list(self):
        self.scrollable_dialog_list = ScrollableDialogList(self, user=self.user)
        self.dialogs_list = self.scrollable_dialog_list.dialogs_list
        self.layout().addWidget(self.scrollable_dialog_list)

    def load_chat_widget(self):
        self.chat = Chat(self, 
                         user=self.user)
        self.layout().addWidget(self.chat)
        self.scrollable_dialog_list.chat = self.chat

    def load_me(self):
        loop = asyncio.get_event_loop()
        self.user = loop.run_until_complete(get_me())

