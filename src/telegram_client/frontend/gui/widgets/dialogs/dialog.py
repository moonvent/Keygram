from datetime import datetime
import os
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from src.config import AVATAR_HEIGHT_IN_DIALOG, AVATAR_WEIGHT_IN_DIALOG, AVATARS_FOLDER_PATH, DIALOG_WIDGET_HEIGHT, DIALOG_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT, MAIN_WIDGET_WIDTH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_text import DialogText
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_title import DialogTitle


class Dialog(_CoreWidget):
    """
        Dialog widget, with one of users
    """
    dialog: TTDialog = None

    dialog_title: DialogTitle = None
    dialog_text: DialogText = None
    dialog_avatar: QLabel = None

    def __init__(self, 
                 parent, 
                 dialog: TTDialog) -> None:
        self.dialog = dialog
        super().__init__(parent)
    
    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        # self.layout().setSpacing(0)
        # self.layout().setContentsMargins(0, 0, 0, 0)

    def load_ui(self):
        self.set_layout()
        # self.setStyleSheet('background-color: green')
        self.setObjectName('dialog')
        self.set_fixed_size(DIALOG_WIDGET_WIDTH, 
                            DIALOG_WIDGET_HEIGHT)
        self.add_dialog_widgets()

    def add_dialog_widgets(self):
        self.add_avatar()

        self.inner_layout = QVBoxLayout(self)
        self.widget_layout.addLayout(self.inner_layout)

        self.add_dialog_title()
        self.add_dialog_text()

    def add_avatar(self):
        self.dialog_avatar = QLabel(self)
        avatar = QPixmap(os.path.join(AVATARS_FOLDER_PATH, f'{self.dialog.id}.jpg'))
        avatar = avatar.scaled(AVATAR_WEIGHT_IN_DIALOG, AVATAR_HEIGHT_IN_DIALOG)
        self.dialog_avatar.setPixmap(avatar)
        self.dialog_avatar.setFixedWidth(AVATAR_WEIGHT_IN_DIALOG)
        self.widget_layout.addWidget(self.dialog_avatar)

    def add_dialog_title(self):
        self.dialog_title = DialogTitle(self, 
                                        dialog=self.dialog)
        self.inner_layout.addWidget(self.dialog_title)

    def add_dialog_text(self):
        self.dialog_text = DialogText(self, 
                                      text=self.dialog.message.text)
        self.inner_layout.addWidget(self.dialog_text)

