from datetime import datetime
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from telethon.tl.custom import dialog
from telethon.tl.custom.dialog import Dialog as TTDialog
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.services.load_internalization import _


class DialogTitle(_CoreWidget):
    """
        Dialog title which contain:
            pinned, status (channel, bot, user), title, muted, [__], amount_unreads, seen_status, last active date
    """
    dialog: TTDialog = None

    pinned_status: QLabel = None
    dialog_type: QLabel = None
    title: QLabel = None
    muted: QLabel = None
    amount_unreads: QLabel = None
    seen_status: QLabel = None
    last_active_time: QLabel = None

    def __init__(self, 
                 parent, 
                 dialog: TTDialog) -> None:
        self.dialog = dialog
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)

    def load_ui(self):
        self.set_layout()

        self.add_pinned_status()
        self.add_dialog_type()
        self.add_title()
        self.add_muted()
        self.add_amount_unread()
        self.add_seen_status()
        self.add_last_active_time()

    def add_pinned_status(self):
        # self.pinned_status = QLabel(self)
        # text = if self.dialog.pinned else 
        # self.pinned_status.setText()
        pass

    def add_dialog_type(self):
        pass

    def add_title(self):
        pass

    def add_muted(self):
        self.muted = QLabel(self)
        mute_date = self.dialog.dialog.notify_settings.mute_until

        if not mute_date or mute_date.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            text = _('not muted')
        else:
            text = _('muted')

        self.muted.setText(text)
        self.layout().addWidget(self.muted)

    def add_amount_unread(self):
        pass

    def add_seen_status(self):
        pass

    def add_last_active_time(self):
        pass

