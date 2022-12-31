from PySide6.QtWidgets import QDoubleSpinBox, QWidget
from telethon.tl.types import Optional
from src.services.database.models.global_data import get_settings, set_setting

from src.config import SPEED_SPINBOX_MAX, SPEED_SPINBOX_MIN, SPEED_STEP, SettingsEnum


class SpeedSpinBox(QDoubleSpinBox):
    
    def __init__(self, parent: Optional[QWidget] = ...) -> None:
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setMaximum(SPEED_SPINBOX_MAX)
        self.setMinimum(SPEED_SPINBOX_MIN)
        self.setSingleStep(SPEED_STEP)
        self.setFixedSize(60, 50)
        self.setValue(get_settings()[SettingsEnum.SPEED.value])
        self.setPrefix('x')

        self.valueChanged.connect(self.change_speed)

    def change_speed(self, new_speed: float):
        set_setting(setting=SettingsEnum.SPEED, 
                    value=new_speed)

