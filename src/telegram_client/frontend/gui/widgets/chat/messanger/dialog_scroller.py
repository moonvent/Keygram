from PySide6.QtWidgets import QScrollBar

from src.telegram_client.frontend.gui.widgets.dialogs.dialog import Dialog


class DialogScroller:
    """
        Class for setup scroll in every dialog, recover it after return to worked dialog, and other
    """
    vertical_scroll: QScrollBar = None
    visited_dialogs: dict[Dialog, int] = None
    
    def recover_scroll(self, 
                       old_dialog):
        """
            Recover scroll value in old dialog
        """
        self.vertical_scroll.setValue(self.visited_dialogs[old_dialog])

    def set_scroll(self, 
                   new_dialog,
                   ):
        """
            Add new dialog to list of visited dialogs
        """
        self.vertical_scroll.setValue(self.vertical_scroll.maximum())
        self.visited_dialogs[new_dialog] = self.vertical_scroll.value()

    def save_dialog_scroll_value(self, 
                                 old_dialog: Dialog):
        """
            Save scroll state after replace current dialog
        """
        self.visited_dialogs[old_dialog] = self.vertical_scroll.value()


