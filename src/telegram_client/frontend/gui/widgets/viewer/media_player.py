from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from src.services.database.models.global_data import get_settings

from src.config import VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH, SettingsEnum


class MediaPlayer(QMediaPlayer):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setup_player()

    def setup_player(self):
        self.audio_output = QAudioOutput()
        # self.player = QMediaPlayer()
        self.setAudioOutput(self.audio_output)
        self.video_output = QVideoWidget()

        self.setVideoOutput(self.video_output)
        self.video_output.setFixedSize(VIDEO_OUTPUT_HEIGHT, VIDEO_OUTPUT_WIDTH)

        self.video_output.mousePressEvent = self.play_media
        self.audio_output.setVolume(get_settings()[SettingsEnum.VOLUME.value])

    def play_media(self, event):
        if self.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def start_video(self, path_to_file: str):
        self.setSource(QUrl.fromLocalFile(path_to_file))
    
        self.play()

        self.parent().set_duration_media()

    def set_handler_on_end_video(self, func):
        self.mediaStatusChanged.connect(func)

