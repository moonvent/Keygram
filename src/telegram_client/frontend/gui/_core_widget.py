from PySide6.QtWidgets import QLayout, QWidget


class _CoreWidget(QWidget):
    """
        Core widget, with need methods which need be override
    """
    widget_layout: QLayout = None

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        """
            Method which load ui for this (self) message
        """
        return NotImplemented

    def set_layout(self):
        """
            Setup the widget layout
        """
        return NotImplemented
     
