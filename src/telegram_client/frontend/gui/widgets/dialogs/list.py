import asyncio
from typing import List
from PySide6.QtWidgets import QVBoxLayout, QWidget
from telethon.tl.custom.dialog import Dialog as TTDialog
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.backend.dialogs.dialogs import get_dialogs
from src.telegram_client.frontend.gui.widgets.dialogs.dialog import Dialog


class DialogList(_CoreWidget):
    """
        Dialog list widget, with inner dialogs
    """
    telethon_dialogs: List[TTDialog] = []
    gui_dialogs: List[Dialog] = []

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)

    def load_ui(self):
        self.set_layout()
        self.load_dialogs_in_ui()

    def load_dialogs_in_ui(self):
        self.load_dialogs_from_telegram()
        self.handle_dialogs()
        a = 1

    def load_dialogs_from_telegram(self):
        """
            Load dialogs from telethon
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_dialogs(dialogs_list=self.telethon_dialogs))

    def handle_dialogs(self):
        for tt_dialog in self.telethon_dialogs:
            gui_dialog = Dialog(self, tt_dialog)
            self.gui_dialogs.append(gui_dialog)

            self.layout().addWidget(gui_dialog)

            

