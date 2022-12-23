from datetime import datetime, timedelta
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from telethon.tl.types import Dialog, User
from telethon.utils import hachoir
from src.config import AVATARS_FOLDER_PATH, INFO_MENU_AVATAR_SIZE, INFO_MENU_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
import os
from src.services.load_internalization import _
from zoneinfo import ZoneInfo
from time import tzname


class InfoMenu(_CoreWidget):
    user: User = None
    _dialog: Dialog = None

    dialog_avatar: QLabel = None

    layout_for_title_and_status: QVBoxLayout = None

    title_label: QLabel = None
    online_status_label: QLabel = None

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
        self.layout().setContentsMargins(5, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setFixedHeight(INFO_MENU_HEIGHT)
        self.setObjectName('info_menu')

    def load_new_dialog(self):
        self.add_avatar()
        self.load_title_and_status()

    def add_avatar(self):
        if not self.dialog_avatar:
            self.dialog_avatar = QLabel(self)
            self.dialog_avatar.setObjectName('info_menu__avatar')
            self.layout().addWidget(self.dialog_avatar)
        avatar = QPixmap(os.path.join(AVATARS_FOLDER_PATH, f'{self.dialog.id}.jpg'))
        avatar = avatar.scaled(INFO_MENU_AVATAR_SIZE, INFO_MENU_AVATAR_SIZE)
        self.dialog_avatar.setPixmap(avatar)
        self.dialog_avatar.setFixedWidth(INFO_MENU_AVATAR_SIZE)

    def load_title_and_status(self):
        self.add_layout_for_title_and_status()
        self.add_title()
        self.add_last_online_status()

    def add_layout_for_title_and_status(self):
        if not self.layout_for_title_and_status:
            self.layout_for_title_and_status = QVBoxLayout(self)
            self.layout_for_title_and_status.setSpacing(0)
            self.layout_for_title_and_status.setContentsMargins(0, 0, 0, 0)
            self.layout().addLayout(self.layout_for_title_and_status)

    def add_title(self):
        if not self.title_label:
            self.title_label = QLabel(self)
            self.title_label.setObjectName('info_menu__title_label')
            self.layout_for_title_and_status.addWidget(self.title_label)

        self.title_label.setText(self.dialog.title)

    def add_last_online_status(self):
        if not self.online_status_label:
            self.online_status_label = QLabel(self)
            self.online_status_label.setObjectName('info_menu__online_status_label')
            self.layout_for_title_and_status.addWidget(self.online_status_label)

        entity = self.dialog.entity

        if not isinstance(entity, User):
            self.online_status_label.setText(f'{entity.participants_count:_} ' + _('subscribers'))
            return

        if hasattr(entity.status, 'expires'):
            self.online_status_label.setText(_('online'))

        else:
            current_tz = ZoneInfo(tzname[0])

            last_online_date = datetime.fromtimestamp(int(entity.status.was_online.timestamp()), 
                                                      ZoneInfo(tzname[0]))

            time_between_now_and_last_online = datetime.now().replace(tzinfo=current_tz) - last_online_date
            last_online_text = _('last_online_status')

            if time_between_now_and_last_online > timedelta(days=7):
                last_online_text += last_online_date.strftime('%H:%M %d.%m.%Y')

            elif time_between_now_and_last_online > timedelta(days=1):
                last_online_text += last_online_date.strftime('%H:%M %d.%m.%Y')

            elif time_between_now_and_last_online > timedelta(hours=1):
                last_online_text += last_online_date.strftime('%H:%M')

            else:
                last_online_text += last_online_date.strftime('%H:%M')

            self.online_status_label.setText(last_online_text)

    # def add_smth_else(self):
    #     ...

