from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.patched import Message
from telethon.tl.types import Channel, User
from src.services.frontend.gui.widgets.dialogs.dialog_cut import cut_text_for_dialogs
from src.config import AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from telethon.tl.custom.dialog import Dialog


class DialogText(_CoreWidget):
    """
        Last message object, which contain:
            text
    """
    text_widget: QLabel = None
    dialog: Dialog = None
    user: User = None
    message: Message = None

    def __init__(self, 
                 parent, 
                 dialog: Dialog,
                 user: User) -> None:
        self.dialog = dialog
        self.message = dialog.message
        self.user = user
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def load_ui(self):
        self.setObjectName('dialog_text')
        # self.setStyleSheet('font-size: 20px')
        self.set_layout()
        self.add_text()

    def add_text(self):
        """
            add preview dialog text
            :param message: if last dialog message was update
        """
        if not self.text_widget:
            self.text_widget = QLabel(self)
            self.text_widget.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.layout().addWidget(self.text_widget)

        self.set_new_text()

    def set_new_text(self, message: Message = None):
        """
            :param message: if last dialog message was update
        """
        if message:
            self.message = message

        text = ''

        if self.dialog.is_group and self.message.sender != self.user:
            if self.message.post_author:
                nickname = self.message.post_author
            elif isinstance(self.message.sender, Channel):
                nickname = self.message.sender.title
            else:
                nickname = self.message.sender.first_name

            if nickname != self.user.first_name:
                text += f'<u>{nickname}</u>: '

        if self.message.video_note:
            text += _('video_message')

        elif self.message.voice:
            text += _('voice_message')

        elif self.message.grouped_id:
            text += _('message_with_group_attachments')

        elif self.message.video:
            text += _('video') + '\n' + self.dialog.message.text

        elif self.message.photo:
            text += _('photo') + '\n' + self.dialog.message.text

        elif self.message.text:
            text += self.message.text

        else:
            text += _('unknown_message_type')
        #
        # elif self.dialog.message.photo and self.dialog.message.photo.grouped_id:
        #     text = _('group_media_message')

        text = cut_text_for_dialogs(text=text, 
                                    max_length=AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT,
                                    with_first_skip=True)

        self.text_widget.setText(text)

