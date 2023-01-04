"""
    One message object describe
"""
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel
from src.services.logging.setup_logger import logger
from telethon.tl.types import Channel, Dialog, User
from src.config import CHAT_COLUMN_WIDTH, CHAT_WIDTH, FONT_NAME, MESSAGE_NAME, MESSAGES_FONT_SIZE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from telethon.tl.patched import Message as TMessage
from zoneinfo import ZoneInfo
from datetime import datetime
from time import tzname

from src.telegram_client.frontend.gui.widgets.chat.messanger.video_message_widget import VideoMessageWidget


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

    title: str = None

    def __init__(self, 
                 parent = None, 
                 message: TMessage = None,
                 user = None,
                 dialog: Dialog = None,
                 msg_number: int = None) -> None:
        self.user = user
        self.message = message
        self.dialog = dialog
        self.msg_number = msg_number

        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QGridLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setColumnStretch(0, 0)
        # self.layout().setColumnStretch(1, 0)
        # self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setFixedWidth(CHAT_COLUMN_WIDTH)

        if self.user:
            self.add_title()
            self.add_send_date()
            self.add_content()

    def add_title(self):
        self.title_label = QLabel(self)

        if not self.message.sender:

            if self.message.sender_id == self.user.id:
                sender = self.user
            else:
                sender = self.dialog.name

        else:
            sender = self.message.sender

        if not isinstance(sender, str):

            if isinstance(sender, User):
                self.title = sender.first_name
            elif self.message.post_author:
                self.title = self.message.post_author
            else:
                self.title = sender.title

        else:
            self.title = sender

        self.title_label.setText(self.title)
        self.layout().addWidget(self.title_label, 0, 1)

    def add_send_date(self):
        self.date_label = QLabel(self)

        current_tz = ZoneInfo(tzname[0])

        send_date = datetime.fromtimestamp(int(self.message.date.timestamp()), 
                                           ZoneInfo(tzname[0]))

        self.date_label.setText(send_date.strftime('%H:%M:%S'))

        if self.message.sender_id == self.user.id:
            index_in_layout = 2
            fixed_width = 57        # for min 40

        else:
            index_in_layout = 0
            fixed_width = 52        # for min 35

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

