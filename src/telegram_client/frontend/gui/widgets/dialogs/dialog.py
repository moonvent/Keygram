"""
    One dialog widget in qt
"""

from datetime import datetime
import os
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from telethon.tl.patched import Message
from telethon.tl.types import User
from telethon.tl.types.messages import PeerDialogs
from src.config import ACTIVE_DIALOG_NAME, AVATAR_HEIGHT_IN_DIALOG, AVATAR_WEIGHT_IN_DIALOG, AVATARS_FOLDER_PATH, DIALOG_ACTIVE_NAME, DIALOG_NAME, DIALOG_WIDGET_HEIGHT, DIALOG_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT, MAIN_WIDGET_WIDTH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_text import DialogText
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_title import DialogTitle


class Dialog(_CoreWidget):
    """
        Dialog widget, with one of users
    """
    dialog: TTDialog = None
    user: User = None

    dialog_title: DialogTitle = None
    dialog_text: DialogText = None
    dialog_avatar: QLabel = None

    active_dialog: bool = False

    inner_layout: QVBoxLayout = None

    def __init__(self, 
                 parent, 
                 dialog: TTDialog,
                 user: User,
                 current_dialog_status: bool = False,
                 message: Message = None) -> None:
        self.dialog = dialog
        self.active_dialog = current_dialog_status
        self.user = user 
        self.message = message
        super().__init__(parent)
    
    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        # self.layout().setSpacing(0)
        # self.layout().setContentsMargins(0, 0, 0, 0)

    def load_ui(self):
        self.set_layout()
        # self.setStyleSheet('background-color: green')
        self.setObjectName(DIALOG_NAME if not self.active_dialog else ACTIVE_DIALOG_NAME)
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
        self.dialog_avatar.setFixedWidth(AVATAR_WEIGHT_IN_DIALOG)
        self.widget_layout.addWidget(self.dialog_avatar)
        
        self.change_avatar_picture()

    def change_avatar_picture(self):
        avatar = QPixmap(os.path.join(AVATARS_FOLDER_PATH, f'{self.dialog.id}.jpg'))
        avatar = avatar.scaled(AVATAR_WEIGHT_IN_DIALOG, AVATAR_HEIGHT_IN_DIALOG)
        self.dialog_avatar.setPixmap(avatar)

    def add_dialog_title(self):
        self.dialog_title = DialogTitle(self, 
                                        dialog=self.dialog,
                                        user=self.user,
                                        message=self.message)
        self.inner_layout.addWidget(self.dialog_title)

    def add_dialog_text(self):
        self.dialog_text = DialogText(self, 
                                      dialog=self.dialog,
                                      user=self.user)
        self.inner_layout.addWidget(self.dialog_text)

    def update_data(self, message: Message):
        if self.objectName() != ACTIVE_DIALOG_NAME:
            self.dialog_title.change_amount_unread()
        self.change_text(message=message)

    def change_text(self, message: Message):
        self.dialog_text.set_new_text(message=message)

    def clear_unread_status(self):
        self.dialog_title.clear_unread_status()

    def change_dialog(self, new_dialog: TTDialog):
        self.dialog = dialog
        self.clear_old_data()
        self.add_dialog_widgets()

    def clear_old_data(self):
        self.dialog_title.deleteLater()
        self.dialog_text.deleteLater()
        self.inner_layout.deleteLater()

