"""
    Viewer vidget for check the media content
"""


import asyncio
import datetime
import os
from pathlib import Path
from PySide6.QtCore import QThread, QUrl, Signal, Slot, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QProgressBar, QSlider, QSpinBox, QStackedLayout, QVBoxLayout
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.services.database.models.global_data import get_settings
from src.config import MEDIA_VIEWER_WIDGET_WIDTH, SPEED_STEP, VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_THUMB_SIZE, VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH, SettingsEnum
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaFormat, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

from src.telegram_client.backend.client_init import client
import time

from src.telegram_client.frontend.gui.widgets.viewer.position_slider import ChangePositionSlider


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

    path_to_file_mp4: str = None

    def run(self) -> None:
        while not os.path.exists(self.path_to_file_mp4):
        # while not os.path.exists(self.path_to_file_mp4) and not Path(self.path_to_file_mp4).stat().st_size:
            ...
        self.signal_to_start.emit()


class ViewerWidget(_CoreWidget):
    video_message: Message = None

    path_to_file_mp4: str = None
    path_to_file_thumb: str = None

    player: QMediaPlayer = None
    video_output: QVideoWidget = None
    audio_output: QAudioOutput = None

    wait_to_load_thread: WaitToLoad = None

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
        #
        # self.change_status_thread = ChangeProgress()
        # self.change_status_thread.current_status.connect(self.change_progress_bar_data)
        # self.change_status_thread.start()

        self.setup_player()

        self.add_timings()
        self.add_change_position()
        self.add_change_speed()

        # self.layout().addStretch()
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)


    def recreate_wtl_thread(self):
        self.wait_to_load_thread = WaitToLoad()
        self.wait_to_load_thread.signal_to_start.connect(self.start_video)

    # def add_load_status(self):
    #     self.progress_bar = QProgressBar(self)
    #     self.progress_bar.setMinimum(0)
    #     self.progress_bar.setMaximum(100)
    #     # self.progress_bar.setFixedSize(VIDEO_OUTPUT_WIDTH, 10)
    #     self.progress_bar.setFixedWidth(VIDEO_OUTPUT_WIDTH)
    #     # self.layout().addWidget(self.progress_bar)

    # def change_progress_bar_data(self, current: int):
    #     self.progress_bar.setValue(current)

    def load_video(self, 
                   path: str,
                   message: Message):
        self.path_to_file_mp4 = path
        self.message = message
        
        if not os.path.exists(self.path_to_file_mp4):
            self.wait_to_load_thread.path_to_file_mp4 = self.path_to_file_mp4
            self.wait_to_load_thread.start()

        else:
            self.start_video()

    def start_video(self):
        self.player.setSource(QUrl.fromLocalFile(self.path_to_file_mp4))
    
        self.player.play()

        self.set_duration_media()

        self.recreate_wtl_thread()

    def setup_player(self):
        self.audioOutput = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audioOutput)
        self.video_output = QVideoWidget()
        self.layout().addWidget(self.video_output)

        self.player.setVideoOutput(self.video_output)
        self.video_output.setFixedSize(VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH)

        self.video_output.mousePressEvent = self.play_media
        
    def play_media(self, event):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def set_duration_media(self):
        self.duration = self.message.media.document.attributes[0].duration
        self.media_duration_label.setText(str(datetime.timedelta(seconds=self.duration)))
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
        self.speed_spinbox.setValue(get_settings()[SettingsEnum.SPEED_STEP.value])
        self.speed_spinbox.setPrefix('x')
        self.layout().addWidget(self.speed_spinbox)

        # self.speed_marker.setFixedWidth(MEDIA_VIEWER_WIDGET_WIDTH)


viewer = None


def generate_viewer():
    global viewer
    if not viewer:
        viewer = ViewerWidget(None)
    return viewer

