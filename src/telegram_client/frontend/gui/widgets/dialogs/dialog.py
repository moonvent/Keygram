from datetime import datetime
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_text import DialogText
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_title import DialogTitle


class Dialog(_CoreWidget):
    """
        Dialog widget, with one of users
    """
    dialog: TTDialog = None
    _dialog_title: DialogTitle = None
    _dialog_text: DialogText = None

    def __init__(self, 
                 parent, 
                 dialog: TTDialog) -> None:
        self.dialog = dialog
        super().__init__(parent)
    
    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)

    def load_ui(self):
        self.set_layout()
        self.add_dialog_widgets()

    def add_dialog_widgets(self):
        self.dialog_title = DialogTitle(self, 
                                        dialog=self.dialog)
        self.dialog_text = DialogText(self, 
                                      text=self.dialog.message.text)

        self.widget_layout.addWidget(self.dialog_title)
        self.widget_layout.addWidget(self.dialog_text)

