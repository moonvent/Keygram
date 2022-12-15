from datetime import datetime
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _


class DialogText(_CoreWidget):
    """
        Last message object, which contain:
            text
    """
    text: str = None

    def __init__(self, 
                 parent, 
                 text: str) -> None:
        self.dialog = dialog
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)

    def load_ui(self):
        self.set_layout()


