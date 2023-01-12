import os
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from src.services.logging.setup_logger import logger
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.config import VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_THUMB_SIZE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.chat.messanger.message.text_message import TextMessage


class PhotoMessage(_CoreWidget):
    user: User = None
    message: Message = None

    path_to_file: str = None
    path_to_thumb: str = None

    thumb_label: QLabel = None
    text_label: TextMessage = None

    viewer: QLabel = None

    additional_contents: list[tuple[str, str]] = None

    media_layout: QVBoxLayout = None

    def __init__(self, 
                 parent, 
                 user: User,
                 message: Message) -> None:
        self.user = user
        self.message = message
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        # self.layout().setAlignment(Qt.AlignHCenter)
        # self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        self.setObjectName('photo_message')

        self.load_content()

        # if self.message.grouped_id:
        #     if self.parent().parent().dialog_gui_messages[self.parent().dialog.id][-1].message.grouped_id == self.message.grouped_id:
        #         logger.critical('Add handle exception on indexes')
        #         ...

        self.setup_thumb()
        self.setup_caption()
        # self.setup_video_player()

    def load_content(self):
        # speed = get_settings()[SettingsEnum.SPEED.value]

        path_to_file_without_ext = os.path.join(VIDEO_MESSAGE_PATH, str(self.message.photo.id))
        self.path_to_thumb = path_to_file_without_ext + '.jpg'
        self.path_to_file = path_to_file_without_ext + '_full.jpg'
        # self.path_to_file_with_need_speed = path_to_file_without_ext + '___speed_coef__.mp4'

        if not os.path.exists(self.path_to_thumb):
            client.download_media(message=self.message,
                                  path=self.path_to_thumb,
                                  thumb=True)

        if not os.path.exists(self.path_to_file):
            client.add_to_downloads(message=self.message,
                                    path=self.path_to_file)

    def setup_thumb(self):
        self.thumb_label = QLabel(self)
        pixmap = QPixmap(self.path_to_thumb)
        # pixmap = pixmap.scaled(240, 120, Qt.KeepAspectRatio)
        self.thumb_label.setFixedSize(pixmap.width(), pixmap.height())
        self.thumb_label.setPixmap(pixmap)
        self.thumb_label.setMargin(20);                                                                                                                   
        self.thumb_label.setScaledContents(True);   

        self.media_layout = QVBoxLayout(self)
        self.media_layout.setSpacing(0)
        self.media_layout.setContentsMargins(0, 0, 0, 0)

        temp = QHBoxLayout(self)
        temp.addWidget(self.thumb_label)

        self.media_layout.addLayout(temp)

        self.layout().addLayout(self.media_layout)

    def setup_caption(self):
        if self.message.text:
            self.text_label = TextMessage(self, 
                                          user=self.user,
                                          message=self.message)
            self.text_label.setObjectName('photo_caption')
            self.layout().addWidget(self.text_label)

    def add_additional_content(self, 
                               message: Message):
        self.download_additional_content(message=message)

        if self.media_layout.count() == 1 or self.media_layout.children()[-1].count() == 2:
            layout = QHBoxLayout(self)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            self.media_layout.addLayout(layout)

        else:
            layout = self.media_layout.children()[-1]

        self.add_new_media(layout=layout)

    def download_additional_content(self, message: Message):
        if not self.additional_contents:
            self.additional_contents = []

        path_to_file_without_ext = os.path.join(VIDEO_MESSAGE_PATH, str(message.photo.id))
        path_to_thumb = path_to_file_without_ext + '.jpg'
        path_to_file = path_to_file_without_ext + '_full.jpg'

        if not os.path.exists(path_to_thumb):
            client.download_media(message=message,
                                  path=path_to_thumb,
                                  thumb=True)

        if not os.path.exists(path_to_file):
            client.add_to_downloads(message=message,
                                    path=path_to_file)

        self.additional_contents.append((path_to_thumb, path_to_file))

    def add_new_media(self, layout: QHBoxLayout):
        layout.addWidget(self.setup_additional_media())

    def setup_additional_media(self):
        thumb_label = QLabel(self)
        path_to_thumb, _ = self.additional_contents[-1]
        pixmap = QPixmap(path_to_thumb)
        pixmap = pixmap.scaled(240, 120, Qt.KeepAspectRatio)
        thumb_label.setFixedSize(pixmap.width(), pixmap.height())
        thumb_label.setPixmap(pixmap)
        thumb_label.setMargin(20);                                                                                                                   
        thumb_label.setScaledContents(True);   

        return thumb_label

