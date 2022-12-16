from PySide6.QtWidgets import QWidget
from src.services.frontend.load_all_styles import load_all_styles_file
from src.config import MAIN_WIDGET_HEIGHT, MAIN_WIDGET_WIDTH, STYLES_FOLDER_PATH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui.widgets.dialogs.list import DialogList


class MainWindow(_CoreWidget):
    """
        Main Window gui widget
    """
    dialogs_list: QWidget = None
    
    def load_ui(self):
        self.set_fixed_size(MAIN_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT)
        self.dialogs_list = DialogList(self)
        self.load_styles()

    def load_styles(self):
        self.setStyleSheet(load_all_styles_file())
