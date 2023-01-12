"""
    Video widget for listening videomessages
"""


import asyncio
from datetime import datetime
import os
from PySide6.QtCore import QThread, QUrl, Signal, Slot, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.services.database.models.global_data import get_settings
from src.config import VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_THUMB_SIZE, SettingsEnum
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaFormat, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from threading import Thread
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.viewer.viewer import ViewerWidget, viewer, generate_viewer


class DownloadVideo(QThread):
    signal_to_set_video: Signal = Signal()

    def __init__(self, 
                 path_to_thumb,
                 path_to_file,
                 message,
                 speed
                 ) -> None:
        super().__init__()
        self.path_to_thumb, self.path_to_file, self.message, self.speed = path_to_thumb, path_to_file, message, speed

    def run(self) -> None:
        if not os.path.exists(self.path_to_thumb):
            client.download_media(message=self.message,
                                  path=self.path_to_thumb,
                                  thumb=True)

        self.signal_to_set_video.emit()

        if not os.path.exists(self.path_to_file):
            client.add_to_downloads(message=self.message,
                                    path=self.path_to_file,
                                    speed=self.speed)

        self.signal_to_set_video.emit()


class VideoMessage(_CoreWidget):
    user: User = None
    video_message: Message = None

    path_to_file_mp4: str = None
    path_to_file_thumb: str = None

    thumb_label: QLabel = None

    viewer: ViewerWidget = None

    download_video_thread: DownloadVideo = None
    
    def __init__(self, 
                 parent, 
                 user: User,
                 video_message: Message) -> None:
        self.user = user
        self.video_message = video_message
        super().__init__(parent)

    def set_layout(self):
        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()

        self.setup_thumb()
        self.load_content()

        # self.setup_video_player()

    def load_content(self):
        speed = get_settings()[SettingsEnum.SPEED.value]
        path_to_file_without_ext = os.path.join(VIDEO_MESSAGE_PATH, self.video_message.file.id)

        self.path_to_file_thumb = path_to_file_without_ext + '.jpg'
        self.path_to_file_mp4 = path_to_file_without_ext + '.mp4'
        self.path_to_file_with_need_speed = path_to_file_without_ext + '___speed_coef__.mp4'

        if not os.path.exists(self.path_to_file_thumb) or not os.path.exists(self.path_to_file_mp4):
            self.download_video_thread = DownloadVideo(path_to_thumb=self.path_to_file_thumb,
                                                       path_to_file=self.path_to_file_mp4,
                                                       message=self.video_message,
                                                       speed=speed)
            self.download_video_thread.signal_to_set_video.connect(self.setup_pixmap)
            self.download_video_thread.start()
        else:
            self.setup_pixmap()

    def setup_thumb(self):
        self.thumb_label = QLabel(self)
        # self.thumb_label.setPixmap(thumb_pixmap)
        self.thumb_label.setFixedSize(VIDEO_MESSAGE_THUMB_SIZE, VIDEO_MESSAGE_THUMB_SIZE)
        self.thumb_label.setObjectName('thumb_video_label')
        self.thumb_label.setMargin(20);                                                                                                                   
        self.thumb_label.setScaledContents(True);   
        self.layout().addWidget(self.thumb_label)
        
        self.thumb_label.mousePressEvent = self.play_video

    def setup_pixmap(self):
        self.thumb_label.setStyleSheet(f"border-image: url('{self.path_to_file_thumb}');")

    def play_video(self, event):
        global viewer
        if not viewer:
            viewer = generate_viewer()

        viewer.load_video(path=self.path_to_file_with_need_speed,
                          message=self.video_message)

