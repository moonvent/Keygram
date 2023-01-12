"""
    Dialog title widget
"""

from datetime import datetime, timedelta
from PySide6 import QtCore
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from src.services.logging.setup_logger import logger
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from telethon.tl.patched import Message
from telethon.tl.types import Channel, User
from src.services.frontend.gui.widgets.dialogs.dialog_cut import cut_text_for_dialogs
from src.config import AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT, AMOUNT_SYMBOLS_FOR_CUTTING_TITLE, AMOUNT_UNREAD_MARK, DIALOG_FONT_SIZE_TITLE, LENGTH_TITLE
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

    message: Message = None

    def __init__(self, 
                 parent, 
                 dialog: TTDialog,
                 user: User
                 ) -> None:
        self.dialog = dialog
        # :TODO: Handle arrived message in execute when it get from channel
        logger.critical('Handle arrived message in execute when it get from channel')
        self.message = dialog.message
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

        self.change_title()

        self.add_pinned_status()

    def change_title(self, dialog: TTDialog = None):
        if dialog:
            self.dialog = dialog

        self.add_amount_unread()
        self.add_seen_status()
        self.add_last_active_time()

    def add_pinned_status(self):
        if not self.pinned_status:
            self.pinned_status = QLabel(self)
            self.pinned_status.setFont(self.get_dialog_title_font())

        if self.dialog.pinned:
            self.pinned_status.setText(_('pinned'))
            self.pinned_status.setFixedWidth(20)
            self.layout().addWidget(self.pinned_status)
            # self.pinned_status.setStyleSheet('background-color: green')

    def add_dialog_type(self):

        if not self.dialog_type:
            self.dialog_type = QLabel(self)
            self.dialog_type.setFont(self.get_dialog_title_font())
            self.layout().addWidget(self.dialog_type)

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

    def add_title(self):
        if not self.title:
            self.title = QLabel(self)
            self.title.setFont(self.get_dialog_title_font())
            self.layout().addWidget(self.title)
        
        title = cut_text_for_dialogs(text=self.dialog.title, 
                                     max_length=AMOUNT_SYMBOLS_FOR_CUTTING_TITLE)
        
        self.title.setText(title)
        self.title.setFixedWidth(LENGTH_TITLE)

    def add_muted(self):
        if not self.muted:
            self.muted = QLabel(self)
            self.muted.setFont(self.get_dialog_title_font())
            self.layout().addWidget(self.muted)

        mute_date = self.dialog.dialog.notify_settings.mute_until

        if not mute_date or mute_date.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            text_code = 'not muted'
        else:
            text_code = 'muted'

        self.muted.setText(_(text_code))
        self.muted.setFixedWidth(20)

    def add_amount_unread(self):
        if not self.amount_unreads:
            self.amount_unreads = QLabel(self)
            self.amount_unreads.setFont(self.get_dialog_title_font())
            self.amount_unreads.setObjectName('dialog_unread')
            self.amount_unreads.setAlignment(QtCore.Qt.AlignCenter)
            self.amount_unreads.setFixedSize(AMOUNT_UNREAD_MARK, AMOUNT_UNREAD_MARK)
            self.layout().addWidget(self.amount_unreads)

        if self.dialog.dialog.unread_mark or self.dialog.unread_count:
            self.amount_unreads.setText(str(self.dialog.unread_count))
            self.amount_unreads.setVisible(True)

        else:
            self.amount_unreads.setVisible(False)

    def add_seen_status(self):
        if self.user.id == self.dialog.id:
            return

        if self.dialog.message.sender_id == self.user.id:

            if not self.seen_status:
                self.seen_status = QLabel(self)
                self.seen_status.setFont(self.get_dialog_title_font())
                self.layout().addWidget(self.seen_status)

            if self.dialog.message.id <= self.dialog.dialog.read_outbox_max_id:
                # if message read by recipient
                text_code = 'seen_status'

            else:
                text_code = 'unseen_status'

            self.seen_status.setText(_(text_code))
            self.seen_status.setVisible(True)

        else:
            if self.seen_status:
                self.seen_status.setVisible(False)

    def add_last_active_time(self):
        if self.dialog.date:
            if not self.last_active_time:
                self.last_active_time = QLabel(self)
                self.last_active_time.setFont(self.get_dialog_title_font())
                self.layout().addWidget(self.last_active_time)

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

            self.last_active_time.setText(text)
            # self.amount_unreads.setFixedWidth(20)

    def clear_unread_status(self):
        if self.amount_unreads:
            self.amount_unreads.setVisible(False)

    def get_dialog_title_font(self):
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSizeF(DIALOG_FONT_SIZE_TITLE)
        return font

    def change_amount_unread(self):
        if not self.amount_unreads.isVisible():
            self.amount_unreads.setText('1')
            self.amount_unreads.setVisible(True)
        else:
            self.amount_unreads.setText(str(int(self.amount_unreads.text()) + 1))

