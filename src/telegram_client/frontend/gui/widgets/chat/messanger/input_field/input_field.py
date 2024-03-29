import PySide6
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QTextEdit, QWidget
from telethon.tl.custom import Dialog
from src.config import INPUT_FIELD_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.keyboard import InputFieldKeyboard
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.vim_widget.vim_edit_widget import VimWidget


class InputField(_CoreWidget,
                 InputFieldKeyboard):
    """
        Input widget
    """
    vim_editor: VimWidget = None
    _dialog: Dialog = None
    main_window: QWidget = None

    def __init__(self, parent) -> None:
        self.main_window = parent.parent()
        super().__init__(parent)

    def set_layout(self):
        self.setLayout(QHBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setFixedHeight(INPUT_FIELD_HEIGHT)
        self.setObjectName('input_field')

        self.add_vim_editor()

        self.set_keyboard_shortcuts()

    def add_vim_editor(self):
        self.vim_editor = VimWidget(self)
        # self.vim_editor.installEventFilter(self)
        self.layout().addWidget(self.vim_editor)

    def send_message(self):
        text = self.vim_editor.text()
        self.vim_editor.clear()
        client.send_message(self.dialog.id, 
                            text)

    def activate(self):
        self.vim_editor.setFocus()
        self.vim_editor.setReadOnly(False)
        self.vim_editor.switch_to_insert_mode()

    def activate_command_mode(self):
        self.vim_editor.switch_to_command_mode_from_insert()

    def close_before_switch_pan(self):
        self.vim_editor.switch_before_change_pan()

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value: Dialog):
        # self.vim_editor.setReadOnly(False)
        self.save_draft()
        self._dialog = value
        self.add_draft_to_textedit(new_dialog=value)

    def add_draft_to_textedit(self, new_dialog: Dialog):
        if text := new_dialog.draft.text:
            self.vim_editor.setText(text)

    def save_draft(self):
        text = self.vim_editor.text()

        if self._dialog:

            if text:
                # if appear new draft
                client.save_draft(dialog=self._dialog,
                                  text=text)
                self.vim_editor.clear()

            elif self._dialog.draft.text:
                # if was draft but now it's not exist
                client.save_draft(dialog=self._dialog,
                                  text='')

    def minimize_field(self):
        self.vim_editor.setReadOnly(True)

    def disable_vim(self):
        # self.vim_editor.set
        ...

