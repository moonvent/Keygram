import os
import re
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.config import MESSAGE_NAME, VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_THUMB_SIZE


class TextMessage(QLabel):
    user: User = None
    message: Message = None

    def __init__(self, 
                 parent, 
                 user: User,
                 message: Message) -> None:
        self.user = user
        self.message = message
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.add_text()
    
    def add_text(self):
        
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSizeF(15)
        self.setFont(font)
        # tl.setFont(font)
        self.setObjectName(MESSAGE_NAME)
        self.setTextFormat(Qt.TextFormat.MarkdownText)

        text = self.message.text

        if '\n**' in text:
            text = re.sub('\n+\*\*', '**\n\n', text)

        self.setText(text)
        self.setWordWrap(True)
        # self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setMargin(5)
        self.adjustSize()

