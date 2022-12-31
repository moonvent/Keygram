from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QSlider, QWidget
from telethon.tl.types import Optional
from src.services.database.models.global_data import get_settings, set_setting

from src.config import VOLUME_SLIDER_MAX, VOLUME_SLIDER_MIN, VOLUME_STEP, SettingsEnum


class VolumeSlider(QSlider):
    audio_output: QAudioOutput = None

    def __init__(self, parent: Optional[QWidget] = ...) -> None:
            super().__init__(parent)
            self.load_ui()

    def load_ui(self):
        self.setOrientation(Qt.Horizontal)
        self.setMaximum(VOLUME_SLIDER_MAX)
        self.setMinimum(VOLUME_SLIDER_MIN)
        self.setSingleStep(VOLUME_STEP)
        # self.speed_spinbox.setFixedSize(60, 50)
        self.setValue(int(get_settings()[SettingsEnum.VOLUME.value] * 100))
        self.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.valueChanged.connect(self.change_volume)

    def change_volume(self):
        new_value = self.value() / 100
        self.audio_output.setVolume(new_value)
        set_setting(setting=SettingsEnum.VOLUME, 
                    value=new_value)
    
