from collections.abc import Callable
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget
from src.services.logging.setup_logger import logger
from src.services.database.models.keymaps import get_keybinds

from src.database.keymaps import Keymaps


class _KeyboardShortcuts:
    """
        Widget which provide interface to create shortcuts
    """
    active_pan: bool = False
    left_pan: QWidget = None
    right_pan: QWidget = None
    up_pan: QWidget = None
    down_pan: QWidget = None

    shortcuts: list[QShortcut] = None

    def set_widget_shortcuts(self):
        """
            Setup widget keyboard shortcut
        """
        self.shortcuts = []

        self.set_keybind_handlers(keybind_title=Keymaps.TO_LEFT_PAN,
                                  method=self.swith_to_left_pan)

        self.set_keybind_handlers(keybind_title=Keymaps.TO_RIGHT_PAN,
                                  method=self.swith_to_right_pan)
        
        self.set_keybind_handlers(keybind_title=Keymaps.TO_UP_PAN,
                                  method=self.swith_to_up_pan)

        self.set_keybind_handlers(keybind_title=Keymaps.TO_DOWN_PAN,
                                  method=self.swith_to_down_pan)

    def set_keybind_handlers(self, 
                             keybind_title: int,
                             method: Callable):
        """
            Method for set need keybind to method
            :param keybinds: tuple of tuples, where in every tuple will be a few keybinds in str format
            :param method: a tuple of method for set every tuple in keybinds to this method

            :example: keybins = (('a', 'b'), ('c', 'd')), methods = (self.activate_up, self.activate_button)
        """

        for keybind in get_keybinds(title=keybind_title):
            # print(keybind, method)
            shortcut = QShortcut(QKeySequence(keybind), self)
            shortcut.activated.connect(method)
            shortcut.setEnabled(False)
            self.shortcuts.append(shortcut)

    def change_pan(func):
        def wrapper(self, *args, **kwargs):

            pan = func(self, *args, **kwargs)

            if pan:
                pan.main_window.active_pan = pan
        
        return wrapper

    @change_pan
    def swith_to_left_pan(self):
        logger.debug(f'Switch to left pan {self.left_pan}')
        return self.left_pan

    @change_pan
    def swith_to_right_pan(self):
        logger.debug(f'Switch to right pan {self.right_pan}')
        return self.right_pan

    @change_pan
    def swith_to_up_pan(self):
        logger.debug(f'Switch to up pan {self.up_pan}')
        return self.up_pan

    @change_pan
    def swith_to_down_pan(self):
        logger.debug(f'Switch to down pan {self.down_pan}')
        return self.down_pan

    def change_pan_shortcuts_state(self, enable: bool):
        """
            Off pan shortcuts when not in pan
        """
        for shortcut in self.shortcuts:
            shortcut.setEnabled(enable)

