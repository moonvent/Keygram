from PySide6.QtWidgets import QHBoxLayout, QLineEdit
from src.config import INPUT_FIELD_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget


class InputField(_CoreWidget):
    """
        Input widget
    """
    line_edit: QLineEdit = None

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
        self.line_edit = QLineEdit(self)
        self.layout().addWidget(self.line_edit)


