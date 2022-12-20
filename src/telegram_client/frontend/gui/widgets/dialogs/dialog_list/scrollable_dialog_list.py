from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import Qt
from src.config import DIALOG_SCROLL_WIDTH, MAIN_WIDGET_HEIGHT, DIALOG_WIDGET_WIDTH

from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.dialog_list import DialogList


class ScrollableDialogList(QScrollArea):
    """
        Make dialog list scrollable
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.dialogs_list = DialogList(self.parent())
        self.setWidget(self.dialogs_list)
        self.setFixedHeight(MAIN_WIDGET_HEIGHT)
        self.verticalScrollBar().setMaximumWidth(DIALOG_SCROLL_WIDTH)
        self.setFixedWidth(DIALOG_WIDGET_WIDTH + DIALOG_SCROLL_WIDTH)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

