from PySide6.QtGui import QTextCursor


class VimSelection:
    additional_select_to_right = False

    def before_select_in_left_direction(self,
                                        cursor: QTextCursor, 
                                        direction: QTextCursor.MoveOperation):
        """
            Prepare to select text in left direction
        """
        if self.visual_mode and not cursor.selectedText() and direction == QTextCursor.MoveOperation.Left:
            cursor.movePosition(QTextCursor.MoveOperation.Right, 
                                QTextCursor.MoveMode.MoveAnchor,
                                n=1,)
            cursor.movePosition(QTextCursor.MoveOperation.Left, 
                                QTextCursor.MoveMode.KeepAnchor,
                                n=1,)

    def clear_selection(self):
        c = self.textCursor()
        c.clearSelection()
        self.setTextCursor(c)

    def add_selected_sym(self, with_redo: bool = False):
        if self.additional_select_to_right:
            # vim cursor logic
            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                    amount_sym=1)
        self.additional_select_to_right = False

        if with_redo:
            self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                    amount_sym=1)

