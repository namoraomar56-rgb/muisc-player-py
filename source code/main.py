import os
import sys

# إخفاء رسالة Pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QPushButton, QLabel, QSlider
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon  


class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Your music player")
        
   
        if os.path.exists("yourmusicplaylogo.png"):
            self.setWindowIcon(QIcon("yourmusicplaylogo.png"))
            
        self.setGeometry(300, 200, 500, 500)
        
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print("error in setup system sound", e) 

      
        self.folder = "music"
        self.is_paused = False

        self.init_ui()  
        self.load_music()  

    def init_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        self.status_label = QLabel("your list select song to play", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px; color: blue;")
        main_layout.addWidget(self.status_label)

        self.song_list = QListWidget(self)
        main_layout.addWidget(self.song_list)

        btn_layout = QHBoxLayout()

        self.play_btn = QPushButton("play", self)
        self.play_btn.clicked.connect(self.play_music)
        btn_layout.addWidget(self.play_btn)

        self.pause_btn = QPushButton("pause", self)
        self.pause_btn.clicked.connect(self.toggle_music)
        btn_layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("stop", self)
        self.stop_btn.clicked.connect(self.stop_music)
        btn_layout.addWidget(self.stop_btn)

        main_layout.addLayout(btn_layout)

        vol_layout = QHBoxLayout()
        vol_label = QLabel("vol level", self)
        vol_layout.addWidget(vol_label)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        pygame.mixer.music.set_volume(0.5)
        

        self.volume_slider.valueChanged.connect(self.change_music)

        vol_layout.addWidget(self.volume_slider)
        main_layout.addLayout(vol_layout)

        central_widget.setLayout(main_layout)

    def load_music(self):
        """Upload MP3 files from the music folder to the menu"""
        self.song_list.clear()
        if not os.path.isdir(self.folder):
            self.status_label.setText(f"the folder '{self.folder}' not exists")
            return
            
        mp3_files = [f for f in os.listdir(self.folder) if f.endswith(".mp3")]

        if not mp3_files:
            self.status_label.setText("folder is empty")
            return

        self.song_list.addItems(mp3_files)    

    def play_music(self):
        """play selected song"""
        selected_item = self.song_list.currentItem()
        if not selected_item:
            self.status_label.setText("please select music!!")
            return

        song_name = selected_item.text()
        file_path = os.path.join(self.folder, song_name)

        if os.path.exists(file_path):
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_paused = False
            self.status_label.setText(f"playing : {song_name}")
            self.pause_btn.setText("pause")   

    def toggle_music(self):
        """Switching between temporary suspension and resumption"""
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.status_label.setText("playing resumed")
            self.pause_btn.setText("pause")
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.status_label.setText("paused")
            self.pause_btn.setText("continue")    

    def stop_music(self):
        """stop"""
        pygame.mixer.music.stop()
        self.is_paused = False
        self.status_label.setText("stopped")

    def change_music(self, value):
        """Adjust the volume level (value between 0.0 and 1.0)"""
        volume = value / 100.0
        pygame.mixer.music.set_volume(volume)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerApp()
    player.show()
    sys.exit(app.exec_())