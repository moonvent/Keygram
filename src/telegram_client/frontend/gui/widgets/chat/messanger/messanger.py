"""
    Messanger in chat
"""
import asyncio
from random import choice, randint
from PySide6 import QtGui
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QLayout, QScrollArea, QScrollBar, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import QRect, QSize, Qt
from telethon.tl.custom import dialog
from telethon.tl.patched import Message as TMessage
from telethon.tl.types import Dialog, User
from src.config import AVATAR_HEIGHT_IN_DIALOG, AVATAR_WEIGHT_IN_DIALOG, AVATARS_FOLDER_PATH, DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH, FONT_NAME, INFO_MENU_AVATAR_SIZE, MAIN_WIDGET_HEIGHT, MESSAGE_NAME, MESSAGES_FONT_SIZE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
import os
from src.telegram_client.backend.client_init import client
from src.telegram_client.backend.chat.messages import get_messages
from src.telegram_client.frontend.gui.widgets.chat.messanger.dialog_scroller import DialogScroller
from src.telegram_client.frontend.gui.widgets.chat.messanger.message import Message


class Messanger(_CoreWidget, 
                DialogScroller):
    """
        Messanger widget
    """
    _dialog: Dialog = None
    user: User = None

    dialog_avatar: QLabel = None

    messages: list[TMessage] = None
    gui_messages: list = None
    
    def __init__(self, 
                 parent,
                 user) -> None:
        self.user = user
        self.visited_dialogs = {}
        super().__init__(parent)

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        old_dialog = self._dialog
        self.save_dialog_scroll_value(old_dialog=old_dialog)

        dialog = self._dialog = value
        self.load_new_dialog()

        if dialog not in self.visited_dialogs:
            self.set_scroll(new_dialog=dialog)
        else:
            self.recover_scroll(old_dialog=dialog)
        
    def set_layout(self):
        self.widget_layout = QGridLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setObjectName('messanger')

    def load_new_dialog(self):
        self.load_messages_from_back()
        self.add_new_messages_to_gui()

        # self.add_avatar()
        #
        # self.add_layout_for_title_and_status()
        # self.add_title()
        # self.add_last_online_status()

    def load_messages_from_back(self):
        loop = asyncio.get_event_loop()
        self.messages = loop.run_until_complete(get_messages(chat_id=self.dialog.id))

    def prepare_to_output_messages(self):
        if not self.gui_messages:
            self.gui_messages = []
            for column_number in range(2):
                self.layout().addWidget(QLabel(self), 0, column_number)

        else:

            for widget in self.gui_messages:

                # if widget.video_widget:
                #     widget.delete_video_widget()

                widget.deleteLater()

            self.gui_messages.clear()

    def add_new_message(self, msg_number: int, message: TMessage):
        message = Message(self,
                          message=message,
                          user=self.user,
                          dialog=self.dialog,
                          msg_number=msg_number)
        self.gui_messages.append(message)
        self.layout().addWidget(message, 
                                msg_number, 
                                1 + (1 if message.message.sender_id == self.user.id else -1)
                                )


    def add_new_messages_to_gui(self):
        self.prepare_to_output_messages()

        for msg_number, message in enumerate(self.messages[::-1]):
            self.add_new_message(msg_number=msg_number,
                                 message=message)
            
