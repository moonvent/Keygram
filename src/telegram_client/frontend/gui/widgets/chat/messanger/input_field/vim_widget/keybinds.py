from typing import Callable
from PySide6.QtGui import QKeyEvent, QKeySequence
from src.services.database.models.keymaps import get_keybinds
from src.database.keymaps import Keymaps


class VimKeybinds:
    """
        Setup widget keybinds
    """
    binds_with_methods: dict[QKeySequence, Callable] = None         # dict, key - shortcut, value - method

    def get_binds_from_db(self, keymap: Keymaps) -> tuple[str, ...]:
        return get_keybinds(title=keymap)

    def pack_in_keysequence(self, binds: tuple[str, ...]) -> tuple[QKeySequence, ...]:
        return tuple(QKeySequence(bind) for bind in binds)

    def create_qt_bind(self, keymap: Keymaps) -> tuple[QKeySequence, ...]:
        binds = get_keybinds(title=keymap)
        return self.pack_in_keysequence(binds=binds)

    def handle_keybind(self, event: QKeyEvent) -> bool:
        """
            Handle pressed keybind, if need to ignore return True
        """
        pressed_key = QKeySequence(event.keyCombination())

        if pressed_key in self.binds_with_methods:
            return self.binds_with_methods[pressed_key]()

