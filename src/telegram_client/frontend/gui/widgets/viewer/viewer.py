"""
    Viewer vidget for check the media content
"""


import asyncio
import datetime
from inspect import isroutine
import os
from pathlib import Path
from threading import Thread
from typing import Optional
from PySide6.QtCore import QObject, QThread, QUrl, Signal, Slot, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QProgressBar, QSlider, QSpinBox, QStackedLayout, QVBoxLayout
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.services.database.models.global_data import get_settings, set_setting
from src.config import MEDIA_VIEWER_WIDGET_WIDTH, SPEED_STEP, VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_THUMB_SIZE, VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH, SettingsEnum
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaFormat, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

from src.telegram_client.backend.client_init import client
import time

from src.telegram_client.frontend.gui.widgets.viewer.position_slider import ChangePositionSlider
from src.telegram_client.backend.chat.video_widget import fastify_video, get_length


# class ChangeProgress(QThread):
#     current_status: Signal = Signal(int)
#     progress: int = None
#
#     def run(self) -> None:
#         # for i in range(1, 100):
#         #     self.current_status.emit(i)
#         #     time.sleep(0.2)
#
#         while True:
#             if self.progress is not None:
#                 # self.progress_bar.setValue(self.current_status)
#                 # if self.current_status == 100:
#                 #     self.current_status = None
#                 print(self.progress)
#                 self.current_status.emit(self.progress)
#
#                 if self.progress == 100:
#                     self.progress = None
#             else:
#                 time.sleep(.1)


class WaitToLoad(QThread):
    signal_to_start = Signal()

    path_to_file: str = None

    def run(self) -> None:
        while not os.path.exists(self.path_to_file):
        # while not os.path.exists(self.path_to_file_mp4) and not Path(self.path_to_file_mp4).stat().st_size:
            ...
        self.signal_to_start.emit()


class WaitToFastify(QThread):
    signal_to_start = Signal()

    path_to_primary_file: str = None
    current_speed: float = None

    def __init__(self, path_to_primary_file: str, speed: float) -> None:
        self.path_to_primary_file = path_to_primary_file
        self.current_speed = speed
        super().__init__()

    def run(self) -> None:
        fastify_video(path=self.path_to_primary_file, speed=self.current_speed)
        self.signal_to_start.emit()


class ViewerWidget(_CoreWidget):
    video_message: Message = None

    path_to_file: str = None
    path_to_file_thumb: str = None

    player: QMediaPlayer = None
    video_output: QVideoWidget = None
    audio_output: QAudioOutput = None

    wait_to_load_thread: WaitToLoad = None
    wait_to_fastify_thread: WaitToFastify = None

    current_timing: str = None
    media_duration: str = None

    current_timing_label: QLabel = None
    media_duration_label: QLabel = None

    # change_status_thread: ChangeProgress = None
    position_slider: QSlider = None
    speed_spinbox: QDoubleSpinBox = None

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        # self.layout().addStretch()
        self.recreate_wtl_thread()
        self.setFixedWidth(MEDIA_VIEWER_WIDGET_WIDTH)

        # self.add_load_status()
        
        self.setup_player()

        self.add_timings()
        self.add_change_position()
        self.add_change_speed()

        # self.layout().addStretch()
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)


    def recreate_wtl_thread(self):
        self.wait_to_load_thread = WaitToLoad()
        self.wait_to_load_thread.signal_to_start.connect(self.start_video)

    def load_video(self, 
                   path: str,
                   message: Message):
        self.path_to_file = path
        self.message = message

        current_speed = self.speed_spinbox.value()
        self.path_to_primary_file = self.path_to_file.replace('___speed_coef__' , '')
        self.path_to_file = self.path_to_file.replace('__speed_coef__', str(current_speed))
        
        if not os.path.exists(self.path_to_file) and os.path.exists(self.path_to_primary_file):
            # if media with need speed doesn't load yet 
            self.wait_to_fastify_thread = WaitToFastify(path_to_primary_file=self.path_to_primary_file,
                                                        speed=current_speed)
            self.wait_to_fastify_thread.signal_to_start.connect(self.start_video)
            # fastify_video(path=self.path_to_primary_file, speed=current_speed)
            self.wait_to_fastify_thread.start()

        else:
            self.start_video()

    def start_video(self):
        self.player.setSource(QUrl.fromLocalFile(self.path_to_file))
    
        self.player.play()

        self.set_duration_media()
        # self.recreate_wtl_thread()

    def setup_player(self):
        self.audioOutput = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audioOutput)
        self.video_output = QVideoWidget()
        self.layout().addWidget(self.video_output)

        self.player.setVideoOutput(self.video_output)
        self.video_output.setFixedSize(VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH)

        self.video_output.mousePressEvent = self.play_media

        self.player.mediaStatusChanged.connect(self.end_of_video)
        
    def play_media(self, event):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def set_duration_media(self):
        self.duration = get_length(path=self.path_to_file)
        self.duration_in_time_format = str(datetime.timedelta(seconds=self.duration))

        self.media_duration_label.setText(self.duration_in_time_format)
        self.position_slider.setMaximum(self.duration)

    def add_timings(self):
        timings_layout = QHBoxLayout(self)
        self.layout().addLayout(timings_layout)
        
        self.start_timing = '00:00'
        self.start_timing_label = QLabel(self)
        self.start_timing_label.setText(self.start_timing)
        timings_layout.addWidget(self.start_timing_label)

        timings_layout.addStretch()

        self.current_timing = '00:00'
        self.current_timing_label = QLabel(self)
        self.current_timing_label.setText(self.current_timing)
        timings_layout.addWidget(self.current_timing_label)

        timings_layout.addStretch()

        self.media_duration = '00:00'
        self.media_duration_label = QLabel(self)
        self.media_duration_label.setText(self.media_duration)
        timings_layout.addWidget(self.media_duration_label)

    def add_change_position(self):
        self.position_slider = ChangePositionSlider(self, 
                                                    player=self.player,
                                                    current_position_label=self.current_timing_label)
        self.layout().addWidget(self.position_slider)

    def add_change_speed(self):
        self.speed_spinbox = QDoubleSpinBox(self)
        self.speed_spinbox.setMaximum(10)
        self.speed_spinbox.setMinimum(0 + SPEED_STEP)
        self.speed_spinbox.setSingleStep(SPEED_STEP)
        self.speed_spinbox.setFixedSize(60, 50)
        self.speed_spinbox.setValue(get_settings()[SettingsEnum.SPEED.value])
        self.speed_spinbox.setPrefix('x')
        self.layout().addWidget(self.speed_spinbox)

        self.speed_spinbox.valueChanged.connect(self.change_speed)

        # self.speed_marker.setFixedWidth(MEDIA_VIEWER_WIDGET_WIDTH)

    def end_of_video(self, status):
        """
            Setup handler on change media status for changing smth
        """
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # change label and slider when video is end
            self.position_slider.setValue(self.position_slider.maximum())
            self.current_timing_label.setText(self.duration_in_time_format)

    def change_speed(self, new_speed: float):
        set_setting(setting=SettingsEnum.SPEED, 
                    value=new_speed)
        

viewer = None


def generate_viewer():
    global viewer
    if not viewer:
        viewer = ViewerWidget(None)
        Thread(target=client.download_all_media, 
               daemon=True).start()
        # create new thred for load all media in background
    return viewer

