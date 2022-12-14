from typing import Callable
from PySide6.QtGui import QKeySequence, QShortcut, Qt
from PySide6.QtWidgets import QFrame, QLayout, QWidget
from src.database.keymaps import Keymaps
from src.services.database.models.keymaps import get_keybinds

from src.services.frontend.load_all_styles import load_all_styles_file


class _CoreWidget(QFrame):
    """
        Core widget, with need methods which need be override
    """
    main_window: QWidget = None

    def __init__(self, 
                 parent) -> None:
        super().__init__(parent)
        self.load_ui()

    def load_styles(self):
        self.setStyleSheet(load_all_styles_file())

    def load_ui(self):
        """
            Method which load ui for this (self) message
        """
        raise NotImplementedError

    def set_layout(self):
        """
            Setup the widget layout
        """
        raise NotImplementedError

    def set_fixed_size(self, 
                       width: int, 
                       height: int):
        """
            Setup widget sizes
        """
        self.setFixedWidth(width)
        self.setFixedHeight(height)

