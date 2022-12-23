from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel
from telethon.tl.types import Dialog, User
from src.config import AVATARS_FOLDER_PATH, INFO_MENU_AVATAR_SIZE, INFO_MENU_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
import os


class InfoMenu(_CoreWidget):
    user: User = None
    _dialog: Dialog = None

    dialog_avatar: QLabel = None

    def __init__(self, parent, user) -> None:
        self.user = user
        super().__init__(parent)

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        self._dialog = value
        self.load_new_dialog()

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setFixedHeight(INFO_MENU_HEIGHT)
        self.setObjectName('info_menu')

    def load_new_dialog(self):
        self.add_avatar()

    def add_avatar(self):
        if not self.dialog_avatar:
            self.dialog_avatar = QLabel(self)
        avatar = QPixmap(os.path.join(AVATARS_FOLDER_PATH, f'{self.dialog.id}.jpg'))
        avatar = avatar.scaled(INFO_MENU_AVATAR_SIZE, INFO_MENU_AVATAR_SIZE)
        self.dialog_avatar.setPixmap(avatar)
        self.dialog_avatar.setFixedWidth(INFO_MENU_AVATAR_SIZE)
        self.layout().addWidget(self.dialog_avatar)

    def add_layout_for_title_and_status(self):
        ...

    def add_title(self):
        ...

    def add_last_online_status(self):
        ...

    # def add_smth_else(self):
    #     ...

