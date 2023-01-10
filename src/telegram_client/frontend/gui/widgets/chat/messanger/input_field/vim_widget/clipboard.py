class VimClipboard:
    """
        Work with vim general clipboard
    """
    command_mode: bool = False
    visual_mode: bool = False
    insert_mode: bool = False

    def cut_selected(self):
        self.add_selected_sym()

        self.switch_to_command_mode()
        self.again_in_insert_mode()

        self.cut()
        return True

    def copy_selected(self):
        if self.visual_mode:
            self.add_selected_sym()

            self.copy()
            self.switch_to_command_mode_from_insert()
            self.add_selected_sym(with_redo=True)

            return True

    def paste_data_after_sym(self):
        if self.command_mode:
            self.additional_select_to_right = True
            self.add_selected_sym()
            self.again_in_insert_mode()
            self.paste()
            self.switch_to_command_mode_from_insert()
            return True

    def paste_data_before_sym(self):
        if self.command_mode:
            # self.add_selected_sym()
            self.again_in_insert_mode()
            self.paste()
            self.switch_to_command_mode_from_insert()
            return True

    def remove_one_sym(self):
        if self.command_mode:
            self.switch_to_command_mode()
            self.again_in_insert_mode()

            self.textCursor().deleteChar()
            self.add_selected_sym(with_redo=True)

            self.switch_to_command_mode_from_insert()
            return True

