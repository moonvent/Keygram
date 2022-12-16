from PySide6.QtWidgets import QFrame, QLayout, QWidget


class _CoreWidget(QFrame):
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

    def set_fixed_size(self, 
                       width: int, 
                       height: int):
        """
            Setup widget sizes
        """
        self.setFixedWidth(width)
        self.setFixedHeight(height)

     
