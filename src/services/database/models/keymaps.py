from sqlalchemy import select
from src.database.keymaps import Keymaps as KeymapsEnum
from src.database.models import Keybinds, Keymaps, session


def get_keymap_by_title(title: KeymapsEnum) -> list[tuple[Keybinds]]:
    """
        Method for get all shortcuts from db in Keybinds model
    """
    query = (select(Keybinds)
             .join(Keymaps)
             .where(Keymaps.title_id == title.value))
    return session.execute(query).fetchall()


def get_from_finded_keybinds_keybind(keybinds: list[tuple[Keybinds]]) -> tuple[str, ...]:
    """
        Method for get all shortcuts from Keybinds model from db
    """
    shortcuts = []
    for keybind in keybinds:
        keybind = keybind[0]
        shortcuts.append(keybind.keybind)
    return tuple(shortcuts)


def get_keybinds(title: KeymapsEnum) -> tuple[str, ...]:
    """
        Method for get all binds by bind title
    """
    keybinds = get_keymap_by_title(title=title)
    return get_from_finded_keybinds_keybind(keybinds=keybinds)

