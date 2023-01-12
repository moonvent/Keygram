from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from telethon.tl.types import Dialog, User
from src.config import DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT

from src.telegram_client.frontend.gui.widgets.chat.messanger.messanger.messanger import Messanger


class ScrolledMessanger(QScrollArea):
    """
        Make messanger srollable
    """
    user: User = None
    _dialog: Dialog = None
    messanger: Messanger = None

    def __init__(self, parent, user) -> None:
        self.user = user
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.messanger = Messanger(self.parent(), 
                                   user=self.user)
        self.messanger.vertical_scroll = self.verticalScrollBar()

        self.setWidget(self.messanger)
        self.setWidgetResizable(True)
        # self.setFixedHeight(MAIN_WIDGET_HEIGHT)
        # self.verticalScrollBar().setMaximumWidth(DIALOG_SCROLL_WIDTH)
        # self.setFixedWidth(DIALOG_WIDGET_WIDTH + DIALOG_SCROLL_WIDTH)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, dialog):
        self._dialog = dialog
        self.messanger.dialog = dialog
 
