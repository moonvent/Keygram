import re

from PySide6.QtGui import QTextCursor



class VimNavigation:
    """
        Setup vim visual mode
    """
    command_mode: bool = False
    visual_mode: bool = False
    insert_mode: bool = False

    def custom_move_cursor(self, 
                           direction: QTextCursor.MoveOperation, 
                           amount_sym: int):
        """
            Custom move cursor method for DRY
        """
        if not self.insert_mode:

            cursor = self.textCursor()

            self.before_select_in_left_direction(cursor=cursor, 
                                                 direction=direction)

            cursor.movePosition(direction, 
                                QTextCursor.MoveMode.KeepAnchor if self.visual_mode else QTextCursor.MoveMode.MoveAnchor,
                                n=amount_sym,
                                )
            self.setTextCursor(cursor)

            if self.visual_mode:
                self.additional_select_to_right = direction == QTextCursor.MoveOperation.Right


    def move_to_back_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[:self.textCursor().position()]
            amount_sym_to_left = len(re.search(r'(\b|\S)\w*\s*$', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                    amount_sym=amount_sym_to_left)


    def move_to_start_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[:self.textCursor().position()]
            amount_sym_to_left = len(re.search(r'[^\s]*\s*$', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                    amount_sym=amount_sym_to_left)

    def move_to_forward_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[self.textCursor().position():]
            amount_sym_to_left = len(re.search(r'^\s*\w*\b', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                    amount_sym=amount_sym_to_left)

    def move_to_end_of_word(self):
        if not self.insert_mode:
            text = self.toPlainText()[self.textCursor().position():]
            amount_sym_to_left = len(re.search(r'^\s*\w*[^\s]*', text).group())

            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                    amount_sym=amount_sym_to_left)

    def move_to_start_of_string(self):
        if not self.insert_mode:
            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                    amount_sym=self.textCursor().position())

    def move_to_end_of_string(self):
        if not self.insert_mode:
            c = self.textCursor()
            
            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                    amount_sym=len(self.text()) - c.position())

