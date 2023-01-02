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
from src.telegram_client.frontend.gui.widgets.viewer.speed_spinbox import SpeedSpinBox
from src.telegram_client.frontend.gui.widgets.viewer.volume_slider import VolumeSlider
from src.telegram_client.frontend.gui.widgets.viewer.media_player import MediaPlayer


class WaitToFastify(QThread):
    signal_to_start = Signal(str)

    path_to_primary_file: str = None
    current_speed: float = None
    path_to_speed_file: str = None

    def __init__(self, path_to_primary_file: str, speed: float) -> None:
        self.path_to_primary_file = path_to_primary_file
        self.current_speed = speed
        super().__init__()

    def run(self) -> None:
        fastify_video(path=self.path_to_primary_file, speed=self.current_speed)
        self.signal_to_start.emit(self.path_to_speed_file)


class VolumeAndSpeed:
    speed_spinbox: SpeedSpinBox = None
    volume_slider: VolumeSlider = None

    def add_change_speed(self):
        self.speed_spinbox = SpeedSpinBox(self)
        self.layout_for_volume_and_speed.addWidget(self.speed_spinbox)
        
    def add_change_volume(self):
        self.volume_slider = VolumeSlider(self)
        self.layout_for_volume_and_speed.addWidget(self.volume_slider)

        self.volume_slider.audio_output = self.player.audio_output
        
    def add_volume_and_speed(self):
        self.layout_for_volume_and_speed = QHBoxLayout(self)
        self.layout().addLayout(self.layout_for_volume_and_speed)
        self.layout_for_volume_and_speed.setSpacing(10)

        self.add_change_volume()
        self.add_change_speed()


class PositionAndTimings:
    path_to_file: str = None

    current_timing_label: QLabel = None
    media_duration_label: QLabel = None

    position_slider: ChangePositionSlider = None

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

    def set_duration_media(self):
        self.duration = get_length(path=self.path_to_file)
        self.duration_in_time_format = str(datetime.timedelta(seconds=self.duration))

        self.media_duration_label.setText(self.duration_in_time_format)
        self.position_slider.setMaximum(self.duration)

    def add_position_slider(self):
        self.position_slider = ChangePositionSlider(self, 
                                                    player=self.player,
                                                    current_position_label=self.current_timing_label)
        self.layout().addWidget(self.position_slider)


class ViewerWidget(_CoreWidget, 
                   VolumeAndSpeed, 
                   PositionAndTimings):
    video_message: Message = None

    path_to_file_thumb: str = None

    player: MediaPlayer = None
    video_output: QVideoWidget = None
    audio_output: QAudioOutput = None

    wait_to_fastify_thread: WaitToFastify = None

    # change_status_thread: ChangeProgress = None

    def set_layout(self):
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def load_ui(self):
        self.set_layout()
        # self.layout().addStretch()
        self.setFixedWidth(MEDIA_VIEWER_WIDGET_WIDTH)

        # self.add_load_status()
        
        self.add_player()

        self.add_timings()
        self.add_position_slider()
        self.add_volume_and_speed()

        # self.layout().addStretch()
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

    def load_video(self, 
                   path: str,
                   message: Message):
        self.path_to_file = path
        self.message = message

        current_speed = self.speed_spinbox.value()
        self.path_to_primary_file = self.path_to_file.replace('___speed_coef__' , '')
        self.path_to_file = self.path_to_file.replace('__speed_coef__', str(current_speed))
        
        if not os.path.exists(self.path_to_primary_file):
            return

        if not os.path.exists(self.path_to_file):
            # if media with need speed doesn't load yet 

            self.wait_to_fastify_thread = WaitToFastify(path_to_primary_file=self.path_to_primary_file,
                                                        speed=current_speed)
            self.wait_to_fastify_thread.path_to_speed_file = self.path_to_file
            self.wait_to_fastify_thread.signal_to_start.connect(self.player.start_video)
            self.wait_to_fastify_thread.start()

        else:
            self.player.start_video(self.path_to_file)

    def add_player(self):
        self.player = MediaPlayer(self)
        self.video_output, self.audio_output = self.player.video_output, self.player.audio_output
        self.player.set_handler_on_end_video(self.end_of_video)
        self.player.set_duration_media = self.set_duration_media
        self.layout().addWidget(self.video_output)

    def end_of_video(self, status):
        """
            Setup handler on change media status for changing smth
        """
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # change label and slider when video is end
            self.position_slider.setValue(self.position_slider.maximum())
            self.current_timing_label.setText(self.duration_in_time_format)



viewer = None


def generate_viewer():
    global viewer

    if not viewer:
        viewer = ViewerWidget(None)
        
    return viewer

