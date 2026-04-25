import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("视频播放器")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)
        
        self.playlist = []
        self.current_index = -1
        self.is_fullscreen = False
        self.normal_geometry = None
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(300, 200)
        main_layout.addWidget(self.video_widget)
        
        control_widget = QWidget()
        control_widget.setMinimumHeight(80)
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(10, 5, 10, 10)
        
        progress_layout = QHBoxLayout()
        
        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet("color: #333; font-size: 12px;")
        progress_layout.addWidget(self.time_label)
        
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setEnabled(False)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #ddd;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 14px;
                height: 14px;
                margin: -4px 0;
                background: #3498db;
                border-radius: 7px;
            }
            QSlider::handle:horizontal:hover {
                background: #2980b9;
            }
        """)
        progress_layout.addWidget(self.progress_slider)
        
        self.duration_label = QLabel("00:00:00")
        self.duration_label.setStyleSheet("color: #333; font-size: 12px;")
        progress_layout.addWidget(self.duration_label)
        
        control_layout.addLayout(progress_layout)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.open_button = QPushButton("打开")
        self.open_button.setMinimumHeight(35)
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        buttons_layout.addWidget(self.open_button)
        
        self.prev_button = QPushButton("后退 5s")
        self.prev_button.setMinimumHeight(35)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        buttons_layout.addWidget(self.prev_button)
        
        self.play_button = QPushButton("播放")
        self.play_button.setMinimumHeight(35)
        self.play_button.setMinimumWidth(80)
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 5px 20px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        buttons_layout.addWidget(self.play_button)
        
        self.next_button = QPushButton("快进 5s")
        self.next_button.setMinimumHeight(35)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        buttons_layout.addWidget(self.next_button)
        
        self.next_video_button = QPushButton("下一个")
        self.next_video_button.setMinimumHeight(35)
        self.next_video_button.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        buttons_layout.addWidget(self.next_video_button)
        
        self.fullscreen_button = QPushButton("全屏")
        self.fullscreen_button.setMinimumHeight(35)
        self.fullscreen_button.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #6c3483;
            }
        """)
        buttons_layout.addWidget(self.fullscreen_button)
        
        buttons_layout.addStretch()
        
        self.current_file_label = QLabel("未选择视频")
        self.current_file_label.setStyleSheet("color: #666; font-size: 12px;")
        self.current_file_label.setMinimumWidth(200)
        buttons_layout.addWidget(self.current_file_label)
        
        control_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(control_widget)
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
    def setup_connections(self):
        self.open_button.clicked.connect(self.open_file)
        self.play_button.clicked.connect(self.toggle_play)
        self.prev_button.clicked.connect(self.skip_backward)
        self.next_button.clicked.connect(self.skip_forward)
        self.next_video_button.clicked.connect(self.play_next_video)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        
        self.progress_slider.sliderMoved.connect(self.set_position)
        
        self.media_player.playbackStateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.errorOccurred.connect(self.handle_error)
        
    def open_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mkv *.mov *.wmv);;所有文件 (*.*)"
        )
        
        if files:
            self.playlist = files
            self.current_index = 0
            self.play_current_video()
            
    def play_current_video(self):
        if self.current_index < 0 or self.current_index >= len(self.playlist):
            return
            
        file_path = self.playlist[self.current_index]
        if os.path.exists(file_path):
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.media_player.play()
            self.play_button.setText("暂停")
            self.progress_slider.setEnabled(True)
            
            file_name = os.path.basename(file_path)
            self.current_file_label.setText(f"正在播放: {file_name}")
            self.setWindowTitle(f"视频播放器 - {file_name}")
            
    def toggle_play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("播放")
        else:
            if self.media_player.source().isEmpty():
                self.open_file()
            else:
                self.media_player.play()
                self.play_button.setText("暂停")
                
    def skip_backward(self):
        if self.media_player.playbackState() != QMediaPlayer.StoppedState:
            position = self.media_player.position()
            new_position = max(0, position - 5000)
            self.media_player.setPosition(new_position)
            
    def skip_forward(self):
        if self.media_player.playbackState() != QMediaPlayer.StoppedState:
            position = self.media_player.position()
            duration = self.media_player.duration()
            new_position = min(duration, position + 5000)
            self.media_player.setPosition(new_position)
            
    def play_next_video(self):
        if not self.playlist:
            QMessageBox.information(self, "提示", "请先添加视频到播放列表")
            return
            
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.play_current_video()
        else:
            QMessageBox.information(self, "提示", "已经是最后一个视频了")
            
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            if self.normal_geometry:
                self.setGeometry(self.normal_geometry)
            self.is_fullscreen = False
            self.fullscreen_button.setText("全屏")
        else:
            self.normal_geometry = self.geometry()
            self.showFullScreen()
            self.is_fullscreen = True
            self.fullscreen_button.setText("退出全屏")
            
    def set_position(self, position):
        self.media_player.setPosition(position)
        
    def media_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_button.setText("暂停")
        else:
            self.play_button.setText("播放")
            
    def position_changed(self, position):
        self.progress_slider.setValue(position)
        self.time_label.setText(self.format_time(position))
        
    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)
        self.duration_label.setText(self.format_time(duration))
        
    def handle_error(self, error, error_string):
        QMessageBox.critical(
            self,
            "错误",
            f"播放错误: {error_string}"
        )
        
    def format_time(self, milliseconds):
        seconds = int(milliseconds / 1000)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggle_play()
        elif event.key() == Qt.Key_Escape and self.is_fullscreen:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_Left:
            self.skip_backward()
        elif event.key() == Qt.Key_Right:
            self.skip_forward()
        elif event.key() == Qt.Key_F:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_N:
            self.play_next_video()
        super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    player = VideoPlayer()
    player.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
