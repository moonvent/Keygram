"""
    Chat window widget
"""
from PySide6.QtWidgets import QVBoxLayout, QPushButton
from telethon.tl.types import Dialog, User
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.frontend.gui.widgets.chat.messanger.info_menu import InfoMenu
from src.telegram_client.frontend.gui.widgets.chat.messanger.scrolled_messanger import ScrolledMessanger
from src.telegram_client.frontend.gui.widgets.chat.messanger.input_field import InputField


class Chat(_CoreWidget):
    """
        Chat widget
    """
    _dialog: Dialog = None
    user: User = None

    info_menu: InfoMenu = None
    
    def __init__(self, 
                 parent,
                 user) -> None:
        self.user = user
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.create_info_menu()
        self.create_messanger()
        self.create_input_field()

    def create_info_menu(self):
        self.info_menu = InfoMenu(self, user=self.user)
        self.layout().addWidget(self.info_menu)

    def create_messanger(self):
        self.messanger = ScrolledMessanger(self, 
                                           user=self.user)
        # self.messanger = Messanger(self, user=self.user)
        self.layout().addWidget(self.messanger)

    def create_input_field(self):
        self.input_field = InputField(self)
        # self.messanger = Messanger(self, user=self.user)
        self.layout().addWidget(self.input_field)

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        self._dialog = value
        self.info_menu.dialog = value
        self.messanger.dialog = value


