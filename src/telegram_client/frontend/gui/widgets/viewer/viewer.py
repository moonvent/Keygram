"""
    Viewer vidget for check the media content
"""


import asyncio
import os
from PySide6.QtCore import QThread, QUrl, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.config import VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_THUMB_SIZE, VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaFormat, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

from src.telegram_client.backend.client_init import client
import time


class ChangeProgress(QThread):
    current_status: Signal = Signal(int)
    progress: int = None

    def run(self) -> None:
        # for i in range(1, 100):
        #     self.current_status.emit(i)
        #     time.sleep(0.2)

        while True:
            if self.progress is not None:
                # self.progress_bar.setValue(self.current_status)
                # if self.current_status == 100:
                #     self.current_status = None
                print(self.progress)
                self.current_status.emit(self.progress)

                if self.progress == 100:
                    self.progress = None
            else:
                time.sleep(.1)


class ViewerWidget(_CoreWidget):
    video_message: Message = None

    path_to_file_mp4: str = None
    path_to_file_thumb: str = None

    video_player: QMediaPlayer = None
    video_output: QVideoWidget = None
    audio_output: QAudioOutput = None

    change_status_thread: ChangeProgress = None

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()

        # self.add_load_status()
        #
        # self.change_status_thread = ChangeProgress()
        # self.change_status_thread.current_status.connect(self.change_progress_bar_data)
        # self.change_status_thread.start()

        self.setup_video_player()

    def add_load_status(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        # self.progress_bar.setFixedSize(VIDEO_OUTPUT_WIDTH, 10)
        self.progress_bar.setFixedWidth(VIDEO_OUTPUT_WIDTH)
        # self.layout().addWidget(self.progress_bar)

    def change_progress_bar_data(self, current: int):
        self.progress_bar.setValue(current)

    def load_video(self, path: str):
        self.path_to_file_mp4 = path
        self.video_player.setSource(QUrl.fromLocalFile(self.path_to_file_mp4))
    
        self.video_player.play()

    def setup_video_player(self):
        self.audioOutput = QAudioOutput()
        self.video_player = QMediaPlayer()
        self.video_player.setAudioOutput(self.audioOutput)
        self.video_output = QVideoWidget()
        self.layout().addWidget(self.video_output)

        self.video_player.setVideoOutput(self.video_output)
        self.video_output.setFixedSize(VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH)
        # self.video_player.play()

        # self.video_output.mousePressEvent = self.play_video
        
    def play_video(self, event):
        self.video_player.play()


viewer = None

def generate_viewer():
    global viewer
    if not viewer:
        viewer = ViewerWidget(None)
    return viewer

