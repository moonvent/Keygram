from PySide6.QtWidgets import QScrollBar

from src.telegram_client.frontend.gui.widgets.dialogs.dialog import Dialog


class DialogScroller:
    """
        Class for setup scroll in every dialog, recover it after return to worked dialog, and other
    """
    vertical_scroll: QScrollBar = None
    visited_dialogs: dict[int, tuple[int, int]] = None       # need tuple with two int, 
                                                             # first it's a last watched state, second it's max, cause 
                                                             # after changing the dialogs need to reset maximum

    conversation_state: bool = True                             # if user message with someone :TODO: make search mode
    
    def recover_scroll(self, 
                       old_dialog: Dialog):
        """
            Recover scroll value in old dialog
        """
        self.vertical_scroll.setRange(0, self.visited_dialogs[old_dialog.id][1])
        self.vertical_scroll.setValue(self.visited_dialogs[old_dialog.id][0])

    def set_scroll(self, 
                   new_dialog: Dialog,
                   ):
        """
            Add new dialog to list of visited dialogs
        """
        maximum = 100_000
        self.vertical_scroll.setRange(0, maximum)   # cause scroll behavior is straight
        self.vertical_scroll.setValue(maximum)
        self.visited_dialogs[new_dialog.id] = [self.vertical_scroll.value(), maximum]

    def save_dialog_scroll_value(self, 
                                 old_dialog: Dialog):
        """
            Save scroll state after replace current dialog
        """
        if old_dialog:
            self.visited_dialogs[old_dialog.id] = [self.vertical_scroll.value(), self.vertical_scroll.maximum()]

