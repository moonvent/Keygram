from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import Qt
from telethon.tl.types import User
from src.config import DIALOG_SCROLL_WIDTH, MAIN_WIDGET_HEIGHT, DIALOG_WIDGET_WIDTH

from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.dialog_list import DialogList
from src.telegram_client.frontend.gui.widgets.chat.chat import Chat


class ScrollableDialogList(QScrollArea):
    """
        Make dialog list scrollable
    """
    user: User = None
    _chat: Chat = None

    def __init__(self, parent, user) -> None:
        self.user = user
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.dialogs_list = DialogList(self.parent(), user=self.user)
        self.dialogs_list.vertical_scroll = self.verticalScrollBar()
        self.setWidget(self.dialogs_list)
        self.setFixedHeight(MAIN_WIDGET_HEIGHT)
        self.verticalScrollBar().setMaximumWidth(DIALOG_SCROLL_WIDTH)
        self.setFixedWidth(DIALOG_WIDGET_WIDTH + DIALOG_SCROLL_WIDTH)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    @property
    def chat(self):
        return self._chat

    @chat.setter
    def chat(self, chat):
        self._chat = chat
        self.dialogs_list.chat = chat
         
