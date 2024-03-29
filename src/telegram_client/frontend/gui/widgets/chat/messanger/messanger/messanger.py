"""
    Messanger in chat
"""
import asyncio
from random import choice, randint
from threading import Thread
import threading
import time
from PySide6 import QtGui
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLayout, QScrollArea, QScrollBar, QSizePolicy, QSpacerItem, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import QRect, QSize, QThread, Qt, Signal
from telethon.tl.custom import dialog
from telethon.tl.patched import Message as TMessage
from telethon.tl.types import Dialog, User
from src.config import AVATAR_HEIGHT_IN_DIALOG, AVATAR_WEIGHT_IN_DIALOG, AVATARS_FOLDER_PATH, DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH, FONT_NAME, INFO_MENU_AVATAR_SIZE, MAIN_WIDGET_HEIGHT, MESSAGE_NAME, MESSAGES_FONT_SIZE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
import os
from src.telegram_client.backend.client_init import client
from src.telegram_client.backend.chat.messages import get_messages
from src.telegram_client.frontend.gui.widgets.chat.messanger.messanger.dialog_scroller import DialogScroller
from src.telegram_client.frontend.gui.widgets.chat.messanger.message.message import Message
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.input_field import InputField
from src.telegram_client.frontend.gui.widgets.chat.messanger.messanger.keyboard import MessangerKeyboard
from src.services.logging.setup_logger import logger
from src.telegram_client.frontend.gui.widgets.chat.messanger.messanger.cache_messages import CachedMessages


class MessageUpdater(QThread):
    get_message_signal = Signal(tuple)

    def run(self) -> None:
        while True:
            if client.new_messages:
                self.get_message_signal.emit(client.new_messages.pop(0))
            time.sleep(0.5)


class Messanger(_CoreWidget, 
                DialogScroller,
                MessangerKeyboard
                ):
    """
        Messanger widget
    """
    _dialog: Dialog = None
    old_dialog: Dialog = None
    user: User = None

    dialog_avatar: QLabel = None

    message: list[TMessage] = None                          # messages from telegram

    gui_messages: list[Message] = None                      # dict for contain current printed messages

    message_updater: MessageUpdater = None                  # thread for update current open dialog

    input_field: InputField = None

    dialog_gui_messages: dict[int, CachedMessages] = {}      # dict for contain all messages with dialog

    current_message_for_visual_index: int = None
    current_selected_messages: list[int] = None

    main_window: QWidget = None
    
    def __init__(self, 
                 parent,
                 user) -> None:
        self.user = user
        self.visited_dialogs = {}
        self.main_window = parent.parent()
        super().__init__(parent)
        self.current_selected_messages = []
        self.load_message_updater()

    def load_message_updater(self):
        self.message_updater = MessageUpdater()
        self.message_updater.get_message_signal.connect(self.update_current_dialog)
        self.message_updater.start()

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        self.old_dialog = self._dialog
        self.save_dialog_scroll_value(old_dialog=self.old_dialog)

        dialog = self._dialog = value
        self.load_new_dialog()

        self.change_scroll_for_new_dialog()

        if self.input_field:
            if value.is_channel and not value.is_group and not value.is_user:
                self.input_field.minimize_field()
            else:
                self.input_field.dialog = dialog

        self.load_styles()

    def set_layout(self):
        # self.widget_layout = QGridLayout(self)
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setObjectName('messanger')
        client.update_current_dialog = self.update_current_dialog

        self.set_keyboard_shortcuts()

    def load_new_dialog(self):
        if self.dialog.id not in self.dialog_gui_messages:
            self.load_messages_from_back()
            self.add_new_messages_to_gui()

        else:
            self.add_old_messages_to_gui()

    def load_messages_from_back(self):
        self.messages = get_messages(chat_id=self.dialog.id)

    def prepare_to_output_messages(self):
        """
            Clear messages from other dialog, and add messages from new
        """
        if not self.gui_messages:
            self.gui_messages = []
            # for column_number in range(2):
                # self.layout().addWidget(QLabel(self), 0, column_number)

        else:
            for widget in self.gui_messages:
                widget.setParent(None)

            self.gui_messages.clear()

    def convert_tg_to_gui_message(self, 
                                  msg_number: int, 
                                  message: TMessage,
                                  dialog: Dialog = None) -> Message:
        """
            Convert tg message to gui message
        """
        return Message(self,
                       message=message,
                       user=self.user,
                       dialog=self.dialog if not dialog else dialog,
                       msg_number=msg_number)

    def add_gui_message_to_layout(self, msg_number: int, gui_message: Message):
        """
            Add gui message to layout
        """
        self.gui_messages.append(gui_message)
        column = 1 + (1 if gui_message.message.sender_id == self.user.id else -1)

        self.current_message_for_visual_index = len(self.gui_messages)

        # self.layout().addWidget(gui_message, 
        #                         msg_number, 
        #                         column)

        message_layout = QHBoxLayout(self)
        self.layout().addLayout(message_layout)

        if gui_message.message.sender_id == self.user.id:
            message_layout.addStretch()
         
        message_layout.addWidget(gui_message)

        if gui_message.message.sender_id != self.user.id:
            message_layout.addStretch()

        
    def add_new_message(self, msg_number: int, message: TMessage):
        """
            Add message from tg to gui
        """
        gui_message = self.convert_tg_to_gui_message(msg_number=msg_number,
                                                     message=message)
        self.add_gui_message_to_layout(msg_number=msg_number, gui_message=gui_message)
        return gui_message

    def add_new_gui_message_to_cache(self, gui_message: Message, dialog_id: int):
        """
            Add new gui message to cache dictionary
        """
        if dialog_id not in self.dialog_gui_messages:
            dgm = self.dialog_gui_messages[dialog_id] = CachedMessages()
        else:
            dgm = self.dialog_gui_messages[dialog_id]

        # if gui_message not in dgm:
        dgm.append(gui_message)

    def add_new_messages_to_gui(self):
        """
            Add to gui messages from telegram
        """
        self.prepare_to_output_messages()
        messages_to_read = []

        for msg_number, message in enumerate(self.messages[::-1]):
            last_message = self.gui_messages and self.gui_messages[-1]

            if message.grouped_id and last_message and message.grouped_id == last_message.message.grouped_id:
                # if it's a group of media
                last_message.add_group_media(message=message)

            else:
                gui_message = self.add_new_message(msg_number=msg_number,
                                                   message=message)
                self.add_new_gui_message_to_cache(gui_message=gui_message,
                                                  dialog_id=self.dialog.id)

            messages_to_read.append(message)
        
        client.make_read_message(dialog=self.dialog, 
                                 messages=messages_to_read)

    def add_old_messages_to_gui(self):
        """
            Add cached messages to gui (if exists new message in conversation, it's alredy be in list)
        """
        self.prepare_to_output_messages()
        messages_to_read = []

        for msg_number, gui_message in enumerate(self.dialog_gui_messages[self.dialog.id]):
            self.add_gui_message_to_layout(msg_number=msg_number,
                                           gui_message=gui_message)
            messages_to_read.append(gui_message.message)

        client.make_read_message(dialog=self.dialog,
                                 messages=messages_to_read)


    def update_current_dialog(self, msg_data: tuple[Dialog, TMessage, int]):
        """
            Add cathed in work time message to dialog 
        """
        dialog, message, dialog_id = msg_data

        if dialog_messages := self.dialog_gui_messages.get(dialog_id):
            msg_number = len(self.gui_messages)
            last_message = self.gui_messages and self.gui_messages[-1]

            if message.grouped_id and last_message and message.grouped_id == last_message.message.grouped_id:
                last_message.add_group_media(message=message)
                
            else:
                gui_message = self.convert_tg_to_gui_message(msg_number=msg_number,
                                                             message=message,
                                                             dialog=dialog)
                dialog_messages.append(gui_message)

                self.change_dialog_scroll_after_update(dialog_id=dialog_id)

                if self.dialog.id == dialog_id:
                    self.add_gui_message_to_layout(msg_number=msg_number,
                                                   gui_message=gui_message)
                    client.mark_read_one_message(message=message)

                    if self.conversation_state:
                        # :TODO: add support group media in active conversation
                        logger.critical('Add support group media in active conversation')
                        # if now going active conversation

                        if self.dialog.id == dialog_id:
                            self.vertical_scroll.setRange(0, self.vertical_scroll.maximum() + 100_000)
                            self.vertical_scroll.setValue(self.vertical_scroll.maximum())

