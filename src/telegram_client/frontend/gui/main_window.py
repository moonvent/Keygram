from PySide6.QtWidgets import QWidget
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui.widgets.dialogs.list import DialogList


class MainWindow(_CoreWidget):
    """
        Main Window gui widget
    """
    dialogs_list: QWidget = None
    
    def load_ui(self):
        self.dialogs_list = DialogList(self)

