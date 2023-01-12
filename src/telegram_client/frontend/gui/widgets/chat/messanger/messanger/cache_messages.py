from telethon.tl.custom import Dialog
from telethon.tl.patched import Message as TMessage


# class CachedMessage:
#     """
#         Type for save message and all message data
#     """
#     tg_message: TMessage = None
#     new_message: bool = False       # message which appear after attach or in converstaion time, which need to read in future
#     gui_message: Message = None
#     dialog: Dialog = None
#
#     def __init__(self, 
#                  tg_message: TMessage = None,
#                  new_message: bool = False,
#                  gui_message: Message = None,
#                  dialog: Dialog = None) -> None:
#         self.tg_message = tg_message
#         self.new_message = new_message
#         self.gui_message = gui_message
#         self.dialog = dialog



class CachedMessages(list):
    """
        Custom list for save messages and other message data
    """
    unread_messages: int = None

    def __init__(self, 
                 message = None):
        super(list).__init__()
        self.unread_messages = 0
        if message:
            self.append(message)
        
