"""
    Dialog title widget
"""

from datetime import datetime, timedelta
from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from telethon.tl.types import User
from src.services.frontend.gui.widgets.dialogs.dialog_cut import cut_text_for_dialogs
from src.config import AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT, AMOUNT_SYMBOLS_FOR_CUTTING_TITLE, AMOUNT_UNREAD_MARK, LENGTH_TITLE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from zoneinfo import ZoneInfo
from time import tzname


class DialogTitle(_CoreWidget):
    """
        Dialog title which contain:
            pinned, status (channel, bot, user), title, muted, [__], amount_unreads, seen_status, last active date
    """
    dialog: TTDialog = None
    user: User = None

    pinned_status: QLabel = None
    dialog_type: QLabel = None
    title: QLabel = None
    muted: QLabel = None
    amount_unreads: QLabel = None
    seen_status: QLabel = None
    last_active_time: QLabel = None

    def __init__(self, 
                 parent, 
                 dialog: TTDialog,
                 user: User
                 ) -> None:
        self.dialog = dialog
        self.user = user
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def load_ui(self):
        self.set_layout()
        self.setObjectName('dialog_title')

        self.add_dialog_type()
        self.add_title()
        self.add_muted()
        self.add_amount_unread()
        self.add_seen_status()
        self.add_last_active_time()
        self.add_pinned_status()

    def add_pinned_status(self):
        self.pinned_status = QLabel(self)
        if self.dialog.pinned:
            self.pinned_status.setText(_('pinned'))
            self.pinned_status.setFixedWidth(20)
            self.layout().addWidget(self.pinned_status)
            # self.pinned_status.setStyleSheet('background-color: green')

    def add_dialog_type(self):
        self.dialog_type = QLabel(self)

        if self.dialog.is_user:
            text_code = 'user'

        elif self.dialog.is_group:
            text_code = 'group'

        elif self.dialog.is_channel:
            text_code = 'channel'

        else:
            text_code = 'bot'

        self.dialog_type.setText(_(text_code))
        self.dialog_type.setFixedWidth(20)

        self.layout().addWidget(self.dialog_type)

    def add_title(self):
        self.title = QLabel(self)
        
        title = cut_text_for_dialogs(text=self.dialog.title, 
                                     max_length=AMOUNT_SYMBOLS_FOR_CUTTING_TITLE)
        
        self.title.setText(title)
        self.title.setFixedWidth(LENGTH_TITLE)
        self.layout().addWidget(self.title)

    def add_muted(self):
        self.muted = QLabel(self)
        mute_date = self.dialog.dialog.notify_settings.mute_until

        if not mute_date or mute_date.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            text_code = 'not muted'
        else:
            text_code = 'muted'

        self.muted.setText(_(text_code))
        self.muted.setFixedWidth(20)

        self.layout().addWidget(self.muted)

    def add_amount_unread(self):
        self.amount_unreads = QLabel(self)

        if self.dialog.dialog.unread_mark or self.dialog.unread_count:

            self.amount_unreads.setObjectName('dialog_unread')
            if self.dialog.unread_count:
                self.amount_unreads.setText(str(self.dialog.unread_count))

            self.amount_unreads.setAlignment(QtCore.Qt.AlignCenter)
            self.amount_unreads.setFixedSize(AMOUNT_UNREAD_MARK, AMOUNT_UNREAD_MARK)
            self.layout().addWidget(self.amount_unreads)

    def add_seen_status(self):
        if self.dialog.message.sender_id == self.user.id and self.user.id != self.dialog.id:
            self.seen_status = QLabel(self)

            if self.dialog.message.id <= self.dialog.dialog.read_outbox_max_id:
                # if message read by recipient
                text_code = 'seen_status'

            else:
                text_code = 'unseen_status'

            self.seen_status.setText(_(text_code))
            self.layout().addWidget(self.seen_status)

    def add_last_active_time(self):
        if self.dialog.date:
            message_date = self.dialog.date.date()

            now = datetime.now()
            today_date = datetime.today().date()
            timestamp = self.dialog.date.timestamp()

            current_tz = ZoneInfo(tzname[0])

            if message_date == today_date:
                handled_date = datetime.fromtimestamp(int(timestamp), ZoneInfo(tzname[0]))
                text = handled_date.strftime('%H:%M')

            else:

                message_date_object_with_tz = datetime.fromtimestamp(int(timestamp), 
                                                                     ZoneInfo(tzname[0]))

                if timedelta(days=1) <= (today_date - message_date) <= timedelta(days=7):
                    text = _(message_date_object_with_tz.strftime('%a'))
                else:
                    text = message_date_object_with_tz.strftime('%d.%m.%y')

            self.last_active_time = QLabel(self)
            self.last_active_time.setText(text)
            # self.amount_unreads.setFixedWidth(20)
            self.layout().addWidget(self.last_active_time)

