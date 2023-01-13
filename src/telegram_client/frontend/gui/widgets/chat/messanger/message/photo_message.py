import os
import time
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Qt, Signal
from src.services.logging.setup_logger import logger
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.config import ADDITIONAL_PHOTO_HEIGHT, ADDITIONAL_PHOTO_WIDTH, VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_THUMB_SIZE, VIDEO_OUTPUT_HEIGHT
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.chat.messanger.message.text_message import TextMessage



class DownloadPhoto(QThread):
    signal_to_set_picture: Signal = Signal()

    def __init__(self, 
                 path_to_thumb,
                 path_to_file,
                 message
                 ) -> None:
        super().__init__()
        self.path_to_thumb, self.path_to_file, self.message = path_to_thumb, path_to_file, message

    def run(self) -> None:
        if not os.path.exists(self.path_to_thumb):
            client.download_media(message=self.message,
                                  path=self.path_to_thumb,
                                  thumb=True)

        if not os.path.exists(self.path_to_file):
            client.add_to_downloads(message=self.message,
                                    path=self.path_to_file)

        self.signal_to_set_picture.emit()


class DownloadFewPhoto(QThread):
    signal_to_set_picture: Signal = Signal(str, str)        # return path to thumb and path to file
    files_to_load: list[tuple[str, str, Message, QLabel]] = None

    def __init__(self) -> None:
        super().__init__()
        self.files_to_load = []

    def run(self) -> None:
        
        while True:
            if not self.files_to_load:
                time.sleep(1)
                continue

            path_to_thumb, path_to_file, message = self.files_to_load.pop(0)
            if not os.path.exists(path_to_thumb):
                client.download_media(message=message,
                                      path=path_to_thumb,
                                      thumb=True)

            if not os.path.exists(path_to_file):
                client.add_to_downloads(message=message,
                                        path=path_to_file)

            self.signal_to_set_picture.emit(path_to_thumb, path_to_file)


class PhotoMessage(_CoreWidget):
    user: User = None
    message: Message = None

    path_to_file: str = None
    path_to_thumb: str = None

    thumb_label: QLabel = None
    text_label: TextMessage = None

    viewer: QLabel = None

    media_layout: QVBoxLayout = None

    download_thread: DownloadPhoto = None
    download_few_photo_thread: DownloadFewPhoto = None

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

        self.setup_thumb()
        self.load_content()

        self.setup_caption()

        if self.message.grouped_id:
            self.download_few_photo_thread = DownloadFewPhoto()
            self.download_few_photo_thread.signal_to_set_picture.connect(self.setup_additional_pixmap)
            self.download_few_photo_thread.start()

    def load_content(self):
        # speed = get_settings()[SettingsEnum.SPEED.value]

        path_to_file_without_ext = os.path.join(VIDEO_MESSAGE_PATH, str(self.message.photo.id))
        self.path_to_thumb = path_to_file_without_ext + '.jpg'
        self.path_to_file = path_to_file_without_ext + '_full.jpg'
        # self.path_to_file_with_need_speed = path_to_file_without_ext + '___speed_coef__.mp4'

        if not os.path.exists(self.path_to_thumb) or not os.path.exists(self.path_to_file):
            self.download_thread = DownloadPhoto(path_to_thumb=self.path_to_thumb,
                                                 path_to_file=self.path_to_file,
                                                 message=self.message)
            self.download_thread.signal_to_set_picture.connect(self.setup_pixmap)
            self.download_thread.start()
            
        else:
            self.setup_pixmap()

    def setup_thumb(self):
        self.thumb_label = QLabel(self)
        self.thumb_label.setFixedSize(VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_SIZE)
        self.thumb_label.setMargin(20);                                                                                        
        self.thumb_label.setScaledContents(True);   

        self.media_layout = QVBoxLayout(self)
        self.media_layout.setSpacing(0)
        self.media_layout.setContentsMargins(0, 0, 0, 0)

        temp = QHBoxLayout(self)
        temp.addWidget(self.thumb_label)

        self.media_layout.addLayout(temp)

        self.layout().addLayout(self.media_layout)

    def setup_pixmap(self):
        pixmap = QPixmap(self.path_to_thumb)
        self.thumb_label.setFixedSize(pixmap.width(), pixmap.height())
        self.thumb_label.setPixmap(pixmap)

    def setup_caption(self):
        if self.message.text:
            self.text_label = TextMessage(self, 
                                          user=self.user,
                                          message=self.message)
            self.text_label.setObjectName('photo_caption')
            self.layout().addWidget(self.text_label)

    def add_additional_content(self, 
                               message: Message):

        if self.media_layout.count() == 1 or self.media_layout.children()[-1].count() == 2:
            layout = QHBoxLayout(self)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            self.media_layout.addLayout(layout)

        else:
            layout = self.media_layout.children()[-1]

        label = self.add_new_media(layout=layout)
        self.download_additional_content(message=message,
                                         label=label)

    def download_additional_content(self, 
                                    message: Message, 
                                    label: QLabel):
        path_to_file_without_ext = os.path.join(VIDEO_MESSAGE_PATH, str(message.photo.id))
        path_to_thumb = path_to_file_without_ext + '.jpg'
        path_to_file = path_to_file_without_ext + '_full.jpg'

        if not os.path.exists(path_to_thumb):
            self.download_few_photo_thread.files_to_load.append((path_to_thumb, 
                                                                 path_to_file,
                                                                 message, 
                                                                 label))
        else:
            self.setup_additional_pixmap(path_to_thumb,
                                         path_to_file,
                                         label)

    def add_new_media(self, layout: QHBoxLayout) -> QLabel:
        # create a patter for set new image in it in a future
        label = self.setup_additional_media()
        layout.addWidget(label)
        return label

    def setup_additional_media(self) -> QLabel:
        thumb_label = QLabel(self)
        thumb_label.setFixedSize(ADDITIONAL_PHOTO_WIDTH, ADDITIONAL_PHOTO_HEIGHT)
        thumb_label.setMargin(20);                                                                                                                   
        thumb_label.setScaledContents(True);   

        return thumb_label

    def setup_additional_pixmap(self,
                                path_to_thumb: str,
                                path_to_file: str,
                                qlabel_ref: QLabel):
        pixmap = QPixmap(path_to_thumb)
        pixmap = pixmap.scaled(ADDITIONAL_PHOTO_WIDTH, 
                               ADDITIONAL_PHOTO_HEIGHT,
                               Qt.KeepAspectRatio)

        qlabel_ref.setPixmap(pixmap)

