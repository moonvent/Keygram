"""
    Slider for change media position
"""
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QLabel, QSlider
from PySide6.QtCore import Qt
from src.config import INTERVAL_TO_CHANGE_POSITION, MEDIA_VIEWER_WIDGET_WIDTH
import datetime
# from src.telegram_client.frontend.gui._core_widget import _CoreWidget


class ChangePositionSlider(QSlider):
    player: QMediaPlayer = None
    play_before_change_position: bool = True
    current_position_label: QLabel = None
    
    def __init__(self, 
                 parent, 
                 player: QMediaPlayer, 
                 current_position_label: QLabel) -> None:
        self.player = player
        self.current_position_label = current_position_label
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        self.setOrientation(Qt.Horizontal)
        self.setFixedWidth(MEDIA_VIEWER_WIDGET_WIDTH)
        # self.setTickPosition(QSlider.TicksAbove)      # doesn't work(((
        self.sliderReleased.connect(self.change_media_position)
        self.sliderMoved.connect(self.slider_moved)
        self.setMaximum(60)

        self.bind_player_bind_to_position()

        self.mousePressEvent = self.mouse_press_event
        self.mouseReleaseEvent = self.mouse_release_event

        self.setTickInterval(INTERVAL_TO_CHANGE_POSITION)

    def change_media_position(self):
        new_position = 1000 * self.value()
        self.player.setPosition(int(new_position))

    def change_slider_by_media_position(self, new_position: int):
        self.current_position_label.setText(str(datetime.timedelta(milliseconds=new_position)).split('.')[0])
        self.setValue(int(new_position / 1000))

    def mouse_press_event(self, event):
        self.unbind_player_bind_to_position()
        super().mousePressEvent(event)

    def mouse_release_event(self, event):
        self.bind_player_bind_to_position()
        self.current_position_label.setText(self.get_text_before_slash()) 
        super().mouseReleaseEvent(event)
        if self.play_before_change_position:
            self.player.play()

    def unbind_player_bind_to_position(self):
        """
            Unbind for correctly change position
        """
        
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.play_before_change_position = True
        self.player.pause()
        self.player.positionChanged.disconnect()

    def bind_player_bind_to_position(self):
        """
            Bind for change slider with video playing
        """
        self.player.positionChanged.connect(self.change_slider_by_media_position)

    def get_text_before_slash(self) -> str:
        return self.current_position_label.text().split(' / ')[0]

    def slider_moved(self, selected_second: int):
        new_selected_second = str(datetime.timedelta(seconds=selected_second))
        self.current_position_label.setText(self.get_text_before_slash() + f' / {new_selected_second}')

