import asyncio
from PySide6.QtGui import QFontDatabase, QKeyEvent
from PySide6.QtWidgets import QHBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from telethon.tl.types import User
from src.services.frontend.load_all_styles import load_all_styles_file
from src.config import DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT, MAIN_WIDGET_WIDTH, STYLES_FOLDER_PATH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.scrollable_dialog_list import ScrollableDialogList
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.chat.chat import Chat
from src.telegram_client.frontend.gui.widgets.viewer.viewer import ViewerWidget, generate_viewer, viewer
import time

from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.dialog_list import DialogList
from src.telegram_client.frontend.gui.modes import Modes


class MainWindow(_CoreWidget,
                 Modes):
    """
        Main Window gui widget
    """
    user: User = None

    dialogs_list: DialogList = None
    chat: Chat = None
    viewer: ViewerWidget = None

    _active_pan: QWidget = None
    pan_before_insert: QWidget = None

    @property
    def active_pan(self):
        return self._active_pan

    @active_pan.setter
    def active_pan(self, new_active_pan):

        if self._active_pan and (self._active_pan != self.chat.input_field):
            # second condition work if already in input field and switch to edit mode in vim
            self.pan_before_insert = self._active_pan
            self._active_pan.change_pan_shortcuts_state(enable=False)

        self._active_pan = new_active_pan

        self._active_pan.change_pan_shortcuts_state(enable=True)
    
    def load_ui(self):

        self.set_fixed_size(MAIN_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT)
        self.set_layout()
        self.load_me()

        self.load_dialogs_list()

        self.load_chat_widget()

        self.load_viewer_vidget()

        self.load_styles()

        self.setup_global_keybinds()
        self.switch_to_command_mode()

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_dialogs_list(self):
        self.scrollable_dialog_list = ScrollableDialogList(self, user=self.user)
        self.dialogs_list = self.scrollable_dialog_list.dialogs_list
        self.layout().addWidget(self.scrollable_dialog_list)

    def load_chat_widget(self):
        self.chat = Chat(self, 
                         user=self.user)
        self.layout().addWidget(self.chat)
        self.scrollable_dialog_list.chat = self.chat

    def load_me(self):
        # client.save_draft()
        self.user = client.get_me()

    def load_viewer_vidget(self):
        global viewer
        viewer = generate_viewer()
        viewer.setParent(self)
        self.viewer = viewer
        self.viewer.setParent(self)
        self.layout().addWidget(self.viewer)

    def setup_global_keybinds(self):
        messanger = self.chat.messanger.messanger

        self.dialogs_list.right_pan = messanger

        self.chat.input_field.up_pan = messanger

        messanger.down_pan = self.chat.input_field
        messanger.left_pan = self.dialogs_list

        self.chat.input_field.left_pan = self.dialogs_list

        self.active_pan = self.dialogs_list

    def keyPressEvent(self, 
                      event: QKeyEvent) -> None:

        match event.key():
            case Qt.Key_Escape:

                if self.command_mode and self.pan_before_insert != self.active_pan:
                    # if press double escape, revert current pan to pan before current pan

                    # if self.active_pan == self.chat.input_field:
                    #     self.chat.input_field.line_edit.clearFocus()

                    # if need, add in prop reset selectable
                    self.active_pan = self.pan_before_insert

                if self.active_pan == self.chat.input_field:
                    self.active_pan.activate_command_mode()

                self.switch_to_command_mode()

            case Qt.Key_V:
                if self.command_mode:
                    self.switch_to_visual_mode()
                elif self.visual_mode:
                    self.switch_to_command_mode()

            case Qt.Key_I:
                # if self.command_mode:
                #     self.switch_to_visual_mode()
                # elif self.visual_mode:
                #     self.switch_to_command_mode()
                self.switch_to_insert_mode()
                self.save_pan_before_input()
                self.chat.input_field.activate()

        return super().keyPressEvent(event)

    def save_pan_before_input(self):
        self.pan_before_insert = self.active_pan
        

