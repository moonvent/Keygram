from PySide6.QtWidgets import QFrame, QLayout, QWidget

from src.services.frontend.load_all_styles import load_all_styles_file


class _CoreWidget(QFrame):
    """
        Core widget, with need methods which need be override
    """
    widget_layout: QLayout = None

    def __init__(self, parent) -> None:
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


class _KeyboardShortcuts:
    """
        Widget which provide interface to create shortcuts
    """

    def set_widget_shortcuts(self):
        """
            Setup widget keyboard shortcut
        """
        raise NotImplementedError
