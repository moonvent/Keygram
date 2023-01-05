from telethon.tl.custom import Dialog
from telethon.tl.patched import Message as TMessage

from telegram_client.frontend.gui.widgets.chat.messanger.message import Message


class CachedMessage:
    """
        Type for save message and all message data
    """
    tg_message: TMessage = None
    new_message: bool = False       # message which appear after attach or in converstaion time, which need to read in future
    gui_message: Message = None
    dialog: Dialog = None

    def __init__(self, 
                 tg_message: TMessage = None,
                 new_message: bool = False,
                 gui_message: Message = None,
                 dialog: Dialog = None) -> None:
        self.tg_message = tg_message
        self.new_message = new_message
        self.gui_message = gui_message
        self.dialog = dialog



class CachedMessages(list):
    """
        Custom list for save messages and other message data
    """
    dialog: Dialog = None
    to_read_messages: list[TMessage] = None

    def __init__(self, 
                 dialog: Dialog = None,
                 message: Message = None):
        super(list).__init__()
        self.to_read_messages = []
        self.append(message)

    def append(self, __object: CachedMessage | Message) -> None:
        is_message = isinstance(__object, Message)
        is_cached_message = isinstance(__object, CachedMessage)

        if not any((is_message, is_cached_message)):
            raise TypeError('Need CacheMessage or Message (from gui module)')

        if is_message:
            object_to_add = CachedMessage(gui_message=__object,
                                          dialog=self.dialog)

        else:
            object_to_add = __object

        return super().append(object_to_add)

        
