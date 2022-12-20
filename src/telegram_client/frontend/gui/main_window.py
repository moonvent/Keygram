from PySide6.QtWidgets import QWidget, QScrollArea
from PySide6.QtCore import Qt
from src.services.frontend.load_all_styles import load_all_styles_file
from src.config import DIALOG_SCROLL_WIDTH, DIALOG_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT, MAIN_WIDGET_WIDTH, STYLES_FOLDER_PATH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui.widgets.dialogs.dialog_list.scrollable_dialog_list import ScrollableDialogList


class MainWindow(_CoreWidget):
    """
        Main Window gui widget
    """
    dialogs_list: QWidget = None
    
    def load_ui(self):
        self.set_fixed_size(MAIN_WIDGET_WIDTH, MAIN_WIDGET_HEIGHT)
        self.load_dialogs_list()
        self.load_styles()

    def load_dialogs_list(self):
        self.scrollable_dialog_list = ScrollableDialogList(self)
        self.dialogs_list = self.scrollable_dialog_list.dialogs_list

