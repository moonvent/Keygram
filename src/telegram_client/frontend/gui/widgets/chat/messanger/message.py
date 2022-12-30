"""
    One message object describe
"""
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel
from telethon.tl.types import Dialog, User
from src.config import FONT_NAME, MESSAGE_NAME, MESSAGES_FONT_SIZE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from telethon.tl.patched import Message as TMessage
from zoneinfo import ZoneInfo
from datetime import datetime
from time import tzname

from src.telegram_client.frontend.gui.widgets.chat.messanger.video_widget import VideoMessageWidget


class Message(_CoreWidget):
    """
        One message object
    """
    message: TMessage = None
    user: User = None
    dialog: Dialog = None
    msg_number: int = None          # message neumber in messanger

    title_label: QLabel = None
    date_label: QLabel = None
    text_label: QLabel = None
    video_message_widget: VideoMessageWidget = None

    def __init__(self, 
                 parent, 
                 message: TMessage,
                 user,
                 dialog: Dialog,
                 msg_number: int) -> None:
        self.user = user
        self.message = message
        self.dialog = dialog
        self.msg_number = msg_number
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QGridLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()

        self.add_title()
        self.add_send_date()
        self.add_content()

    def add_title(self):
        self.title_label = QLabel(self)
        self.title_label.setText(self.message.sender.first_name)
        self.layout().addWidget(self.title_label, 0, 1)

    def add_send_date(self):
        self.date_label = QLabel(self)

        current_tz = ZoneInfo(tzname[0])

        send_date = datetime.fromtimestamp(int(self.message.date.timestamp()), 
                                           ZoneInfo(tzname[0]))

        self.date_label.setText(send_date.strftime('%H:%M'))

        if self.message.sender_id == self.user.id:
            index_in_layout = 2
            fixed_width = 40

        else:
            index_in_layout = 0
            fixed_width = 35

        self.date_label.setFixedWidth(fixed_width)
        self.layout().addWidget(self.date_label, 1, index_in_layout)

    def add_content(self):
        if self.message.video_note:
            self.load_video_message()
        else:
            self.add_text()

    def add_text(self):
        tl = self.text_label = QLabel(self)
        font = QFont(FONT_NAME)
        font_size = MESSAGES_FONT_SIZE

        font.setPointSize(font_size)

        tl.setFont(font)
        tl.setObjectName(MESSAGE_NAME)
        tl.setText(self.message.text)
        tl.setWordWrap(True)
        tl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        tl.setMargin(5)
        tl.adjustSize()
        self.layout().addWidget(tl, 1, 1)

    def load_video_message(self):
        self.video_message_widget = VideoMessageWidget(self,
                                                       user=self.user,
                                                       video_message=self.message)
        self.layout().addWidget(self.video_message_widget, 1, 1)

