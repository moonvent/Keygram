from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QTextEdit
from src.config import INPUT_FIELD_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _


class InputField(_CoreWidget):
    """
        Input widget
    """
    line_edit: QTextEdit = None

    def set_layout(self):
        self.setLayout(QHBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setFixedHeight(INPUT_FIELD_HEIGHT)
        self.setObjectName('input_field')

        self.add_line_edit()

    def add_line_edit(self):
        self.line_edit = QTextEdit(self)
        self.line_edit.setPlaceholderText(_('write_message'))
        self.line_edit.setObjectName('input_field')
        self.line_edit.setFixedHeight(INPUT_FIELD_HEIGHT)
        # self.line_edit.setTextMargins(20, 0, 0, 0)
        self.layout().addWidget(self.line_edit)


