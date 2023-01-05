import PySide6
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QTextEdit
from telethon.tl.custom import Dialog
from src.config import INPUT_FIELD_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field.keyboard import InputFieldKeyboard


class InputField(_CoreWidget,
                 InputFieldKeyboard):
    """
        Input widget
    """
    line_edit: QTextEdit = None
    dialog: Dialog = None

    def set_layout(self):
        self.setLayout(QHBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setFixedHeight(INPUT_FIELD_HEIGHT)
        self.setObjectName('input_field')

        self.add_line_edit()

        self.set_widget_shortcuts()

    def add_line_edit(self):
        self.line_edit = QTextEdit(self)
        self.line_edit.setPlaceholderText(_('write_message'))
        self.line_edit.setObjectName('input_field')
        self.line_edit.setFixedHeight(INPUT_FIELD_HEIGHT)
        self.line_edit.setCursorWidth(100)
        # self.line_edit.setTextMargins(20, 0, 0, 0)
        self.line_edit.installEventFilter(self)
        self.layout().addWidget(self.line_edit)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Return and self.line_edit.hasFocus():
            self.send_message()
        return super().keyPressEvent(event)

    # def eventFilter(self, 
    #                 watched: QObject, 
    #                 event: QEvent) -> bool:
    #     if event.type() == QEvent.KeyPress and watched is self.line_edit:
    #         if event.key() == Qt.Key_Return and self.line_edit.hasFocus():
    #             self.send_message()
    #
    #     return super().eventFilter(watched, event)

    def send_message(self):
        text = self.line_edit.toPlainText()
        self.line_edit.clear()
        client.send_message(self.dialog.id, 
                            text)

