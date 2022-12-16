from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from src.services.frontend.gui.widgets.dialogs.dialog_cut import cut_text_for_dialogs
from src.config import AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _


class DialogText(_CoreWidget):
    """
        Last message object, which contain:
            text
    """
    text_widget: QLabel = None
    text: str = None

    def __init__(self, 
                 parent, 
                 text) -> None:
        self.text = text
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def load_ui(self):
        self.set_layout()
        self.add_text()

    def add_text(self):
        self.text_widget = QLabel(self)

        text = cut_text_for_dialogs(text=self.text, 
                                    max_length=AMOUNT_SYMBOLS_FOR_CUTTING_MESSAGE_TEXT)

        self.text_widget.setText(text)
        self.text_widget.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.layout().addWidget(self.text_widget)

