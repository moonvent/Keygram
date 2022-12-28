"""
    Video widget for listening videomessages
"""


import asyncio
from datetime import datetime
import os
from PySide6.QtCore import QUrl, Slot, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel
from telethon.tl.patched import Message
from telethon.tl.types import User
from src.config import VIDEO_MESSAGE_PATH, VIDEO_MESSAGE_SIZE, VIDEO_MESSAGE_THUMB_SIZE
from src.telegram_client.frontend.gui._core_widget import _CoreWidget
from PySide6.QtMultimedia import QAudio, QAudioOutput, QMediaFormat, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from threading import Thread
from src.telegram_client.backend.client_init import client
from src.telegram_client.frontend.gui.widgets.viewer.viewer import ViewerWidget, viewer, generate_viewer
from src.services.frontend.gui.widgets.chat.messanger.video_widget import message_with_media_to_load
from src.telegram_client.backend.chat.download_files import download_file


class VideoMessageWidget(_CoreWidget):
    user: User = None
    video_message: Message = None

    path_to_file_mp4: str = None
    path_to_file_thumb: str = None

    # video_player: QMediaPlayer = None
    # video_output: QVideoWidget = None
    # audio_output: QAudioOutput = None

    thumb_label: QLabel = None

    viewer: ViewerWidget = None
    
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

        self.load_content()

        self.setup_thumb()
        # self.setup_video_player()

    def load_content(self):
        self.path_to_file_thumb = os.path.join(VIDEO_MESSAGE_PATH, f'{self.video_message.sender_id}/{self.video_message.id}.jpg')
        self.path_to_file_mp4 = os.path.join(VIDEO_MESSAGE_PATH, f'{self.video_message.sender_id}/{self.video_message.id}.mp4')

        if not os.path.exists(self.path_to_file_thumb):

            client.download_media(message=self.video_message,
                                  path=self.path_to_file_thumb,
                                  thumb=True)
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(self.load_thumb())

        # if not os.path.exists(self.path_to_file_mp4):
            # Thread(target=asyncio.run, args=(self.download_video(),)).start()

            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(self.download_video())

        if not os.path.exists(self.path_to_file_mp4):
            client.add_to_downloads(message=self.video_message,
                                    path=self.path_to_file_mp4)

    # async def load_thumb(self):
    #     self.path_to_file_thumb = os.path.join(VIDEO_MESSAGE_PATH, f'{self.video_message.sender_id}/{self.video_message.id}.jpg')
    #
    #     if not os.path.exists(self.path_to_file_thumb):
    #         await self.video_message.download_media(self.path_to_file_thumb, thumb=-1)      # for download only thumb

    def output_download_process(self, current, total):
        # print('Downloaded', current, 'out of', total,
        #       'bytes: {:.2%}'.format(current / total))
        current_in_percent = int((100 * current) / total)
        self.viewer.change_status_thread.progress = current_in_percent
        # self.viewer.change_progress_bar_data(current_in_percent)

    # async def download_video(self):
    #     # self.video_message.download_media(self.path_to_file_mp4)  # it doesn't work correctly
    #     with open(self.path_to_file_mp4, 'wb') as file:
    #         await download_file(client, self.video_message.document, file)
    
    # def download_video(self):
    #     # message_with_media_to_load.append((self.path_to_file_mp4, self.video_message))
    #     # self.viewer = generate_viewer()
    #
    #     async def download_video_async():
    #         await self.video_message.download_media(self.path_to_file_mp4, 
    #                                                 # progress_callback=self.output_download_process
    #                                                 )
    #
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(download_video_async())

    def setup_thumb(self):
        self.thumb_label = QLabel(self)
        # self.thumb_label.setPixmap(thumb_pixmap)
        self.thumb_label.setFixedSize(VIDEO_MESSAGE_THUMB_SIZE, VIDEO_MESSAGE_THUMB_SIZE)
        self.thumb_label.setObjectName('thumb_label')
        self.thumb_label.setMargin(20);                                                                                                                   
        self.thumb_label.setStyleSheet(f"border-image: url('{self.path_to_file_thumb}');")
        self.thumb_label.setScaledContents(True);   
        self.layout().addWidget(self.thumb_label)
        
        self.thumb_label.mousePressEvent = self.play_video

    def play_video(self, event):

        # print(self.path_to_file_mp4)
        global viewer
        if not viewer:
            viewer = generate_viewer()

        viewer.load_video(path=self.path_to_file_mp4,
                          message=self.video_message)

        # client.download_all_media(start_media_path=self.path_to_file_mp4)

        # if not os.path.exists(self.path_to_file_mp4):
        #     self.download_video()

        # viewer.start()
        # self.video_player.play()

