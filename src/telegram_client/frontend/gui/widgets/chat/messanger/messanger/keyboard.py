from typing import Literal
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget
from src.config import NOT_SELECTED_MESSANGE_CSS_CLASS, SELECTED_MESSANGE_CSS_CLASS
from src.database.keymaps import Keymaps
from src.telegram_client.frontend.gui._keyboard_shortcuts import _KeyboardShortcuts
from src.telegram_client.frontend.gui.widgets.chat.messanger.message import Message


UP_DIRECTION = 'up'
DOWN_DIRECTION = 'down'


class MessangerKeyboard(_KeyboardShortcuts):

    old_select_index: int = None
    select_direction: Literal['up', 'down'] = None

    def set_keyboard_shortcuts(self):
        super().set_widget_shortcuts()

        self.set_keybind_handlers(keybind_title=Keymaps.DOWN_IN_MESSANGER_LIST,
                                  method=self.activate_message_below)

        self.set_keybind_handlers(keybind_title=Keymaps.UP_IN_DIALOGS_LIST,
                                  method=self.activate_message_above)

    def reset_selection(self):
        self.select_direction = self.old_select_index = None

        for message in self.current_selected_messages:
            if message == self.gui_messages[self.current_message_for_visual_index]:
                continue
            message.setObjectName(NOT_SELECTED_MESSANGE_CSS_CLASS)

        self.current_selected_messages.clear()
        # self.current_message_for_visual_index = len(self.gui_messages)

    def paint_all_row(self, css_class: str, need_to_paint_index: int = None):
        if need_to_paint_index:
            gui_message = self.gui_messages[need_to_paint_index]
        else:
            gui_message = self.gui_messages[self.current_message_for_visual_index]
        gui_message.setObjectName(css_class)

        # for i in range(3):
        #     item = self.layout().itemAtPosition(self.current_message_for_visual_index, i)
        #     item.setObjectName(css_class)


    def add_to_selected(self, message_index: int):
        """
            Repaint selected messages and IF IN VISUAL MODE do smth extra work
        """

        gui_message = self.gui_messages[message_index]
        self.paint_all_row(css_class=SELECTED_MESSANGE_CSS_CLASS,
                           need_to_paint_index=message_index)

        if self.main_window.visual_mode:
            self.current_selected_messages.append(gui_message)

    def remove_from_selected(self, message_index: int, from_list_too: bool = False):
        """
            Repaint selected messages and IF IN VISUAL MODE do smth extra work
        """

        if from_list_too:
            self.current_selected_messages.remove(self.gui_messages[message_index])

        if (message_index < len(self.gui_messages) and not self.main_window.visual_mode) or from_list_too:
            self.paint_all_row(css_class=NOT_SELECTED_MESSANGE_CSS_CLASS, 
                               need_to_paint_index=message_index)

    def start_selecting_new_messages(self, swap_direction: bool = False):
        if not self.current_selected_messages or swap_direction:
            # if start select messages
            self.add_to_selected(message_index=self.old_select_index)

            if swap_direction:
                if self.current_message_for_visual_index > self.old_select_index:
                    self.current_message_for_visual_index = self.old_select_index
                    self.old_select_index -= 1
                else:
                    self.current_message_for_visual_index = self.old_select_index
                    self.old_select_index += 1

        if not swap_direction:
            self.add_to_selected(message_index=self.current_message_for_visual_index)

    def work_with_selection(self):
        """
            Work with select or deselect item, IF IN VISUAL MODE ONLY
        """
        if self.main_window.visual_mode:

            if not self.select_direction:

                if self.current_message_for_visual_index < self.old_select_index:
                    self.select_direction = UP_DIRECTION
                else:
                    self.select_direction = DOWN_DIRECTION

            if (self.select_direction == UP_DIRECTION and self.current_message_for_visual_index < self.old_select_index) or \
                    (self.select_direction == DOWN_DIRECTION and self.current_message_for_visual_index > self.old_select_index):
                self.start_selecting_new_messages()

            elif (self.select_direction == DOWN_DIRECTION and self.current_message_for_visual_index < self.old_select_index and not(self.current_selected_messages)) or \
                    (self.select_direction == UP_DIRECTION and self.current_message_for_visual_index > self.old_select_index and not(self.current_selected_messages)):
                
                self.select_direction = UP_DIRECTION if self.select_direction == DOWN_DIRECTION else DOWN_DIRECTION
                self.start_selecting_new_messages(swap_direction=True)

            else:
                self.remove_from_selected(message_index=self.old_select_index, 
                                          from_list_too=True)

    def switch_message(func):
        """
            Change dialog style and reload it
        """

        def wrapped(self, *args, **kwargs):
            if not self.main_window:
                self.main_window = self.parent().parent().parent().parent()
            
            if not self.main_window.visual_mode:
                self.remove_from_selected(message_index=self.current_message_for_visual_index)

            func(self, *args, **kwargs)

            if not self.main_window.visual_mode:
                self.add_to_selected(message_index=self.current_message_for_visual_index)

            self.work_with_selection()

            self.load_styles()

        return wrapped

    @switch_message
    def activate_message_above(self):
        if self.current_message_for_visual_index > 0:
            self.old_select_index = self.current_message_for_visual_index
            self.current_message_for_visual_index -= 1
        # active_dialog_index = self.gui_dialogs.index(self.active_dialog)
        #
        # if active_dialog_index == 0:        # for infine scroll
        #     return
        #
        # else:
        #     self.active_dialog = self.gui_dialogs[active_dialog_index - 1]
        #
        # if active_dialog_index <= self.index_to_continue_scroll_up:
        #     self.vertical_scroll.setValue(self.vertical_scroll.value() - DIALOG_WIDGET_HEIGHT)
        #     if active_dialog_index != 1:
        #         self.index_to_continue_scroll_up -= 1
        #         self.index_to_continue_scroll_down -= 1
        
    @switch_message
    def activate_message_below(self):
        if self.current_message_for_visual_index < (len(self.gui_messages) - 1):
            self.old_select_index = self.current_message_for_visual_index
            self.current_message_for_visual_index += 1
        # active_dialog_index = self.gui_dialogs.index(self.active_dialog)
        #
        # if active_dialog_index == len(self.gui_dialogs) - 1:        # for infine scroll
        #     return
        #     
        # else:
        #     self.active_dialog = self.gui_dialogs[active_dialog_index + 1]
        #
        # if active_dialog_index >= self.index_to_continue_scroll_down:
        #     self.vertical_scroll.setValue(self.vertical_scroll.value() + DIALOG_WIDGET_HEIGHT)
        #     if (len(self.gui_dialogs) - 2) != active_dialog_index:
        #         self.index_to_continue_scroll_down += 1
        #         self.index_to_continue_scroll_up += 1

