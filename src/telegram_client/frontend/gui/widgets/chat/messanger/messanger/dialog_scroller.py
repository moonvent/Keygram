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
        old_dialog_data = self.visited_dialogs[old_dialog.id]
        self.vertical_scroll.setRange(0, old_dialog_data[1])
        self.vertical_scroll.setValue(old_dialog_data[0])

    def set_scroll(self, 
                   new_dialog: Dialog,
                   ):
        """
            Add new dialog to list of visited dialogs
        """
        maximum = 100_000
        self.vertical_scroll.setRange(0, maximum)   # cause scroll behavior is straight
        self.vertical_scroll.setValue(maximum)
        self.visited_dialogs[new_dialog.id] = (self.vertical_scroll.value(), maximum)

    def save_dialog_scroll_value(self, 
                                 old_dialog: Dialog):
        """
            Save scroll state after replace current dialog
        """
        if old_dialog:
            self.visited_dialogs[old_dialog.id] = (self.vertical_scroll.value(), self.vertical_scroll.maximum())

    def change_scroll_for_new_dialog(self):
        """
            Change scroll position for new dialog
        """

        dialog = self.dialog

        if dialog.id not in self.visited_dialogs:
            self.set_scroll(new_dialog=dialog)
        else:
            self.recover_scroll(old_dialog=dialog)

    def change_dialog_scroll_after_update(self, dialog_id: int):
        maximum = 100_000
        self.visited_dialogs[dialog_id] = (maximum, maximum)
        
