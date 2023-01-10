from enum import IntEnum

from PySide6.QtGui import QTextCursor


class InsertType(IntEnum):
    """
        Type of insert modes
    """
    StartOfString = 1
    CurrentSymbol = 2
    NextSymbol = 3
    EndOfString = 4


class VimInsert:
    """
        Work with insert command
    """
    command_mode: bool = False
    visual_mode: bool = False
    insert_mode: bool = False

    def again_in_insert_mode(self,
                             to_position: InsertType = InsertType.CurrentSymbol):
        if self.command_mode:
            self.setReadOnly(False)
            self.setCursorWidth(1)

            match to_position:
                case to_position.NextSymbol:
                    self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                            amount_sym=1)

                case to_position.StartOfString:
                    self.custom_move_cursor(direction=QTextCursor.MoveOperation.Left,
                                            amount_sym=self.textCursor().position()
                                            )

                case to_position.EndOfString:
                    self.custom_move_cursor(direction=QTextCursor.MoveOperation.Right,
                                            amount_sym=len(self.toPlainText()) - self.textCursor().position()
                                            )

            self.switch_to_insert_mode()
            return True

