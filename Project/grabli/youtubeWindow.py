from PyQt5 import QtCore, QtGui, QtWidgets
from youtube import *
from configs import *
import requests
import re
import os


class VideoInfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    #TODO Add label (CommentsCounter) represented amount of comments that will be downloaded
    #TODO Add choiseBox (UsingReplyComents) ? (yes) downloand with all reply comments : (no) download without. Deafualt true , connected with (CommentsCounter)

    def init_ui(self):
        self.setWindowTitle("YouTube Comments")
        self.resize(634, 460)

        layout = QtWidgets.QVBoxLayout(self)

        self.url_input = QtWidgets.QLineEdit(self)
        self.url_input.setPlaceholderText("Enter YouTube video URL")
        layout.addWidget(self.url_input)

        self.find_button = QtWidgets.QPushButton("Find Video", self)
        self.find_button.clicked.connect(self.find_video)
        layout.addWidget(self.find_button)

        self.video_info_group = QtWidgets.QGroupBox("Video Info", self)
        self.video_info_layout = QtWidgets.QVBoxLayout(self.video_info_group)

        self.title_label = QtWidgets.QLabel("Title: ", self)
        self.video_info_layout.addWidget(self.title_label)

        self.author_label = QtWidgets.QLabel("Author: ", self)
        self.video_info_layout.addWidget(self.author_label)

        self.thumbnail_label = QtWidgets.QLabel(self)
        self.thumbnail_label.setFixedSize(320, 180)
        self.video_info_layout.addWidget(self.thumbnail_label)

        layout.addWidget(self.video_info_group)

        self.download_button = QtWidgets.QPushButton("Download Comments", self)
        self.download_button.clicked.connect(self.download_comments)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def find_video(self):
        print("start")
        try:
            video_url = self.url_input.text()
            video_id = self.extract_video_id(video_url)
            api_key = YOUTUBE_API
            print(video_url , video_id , api_key)
            if video_id:
                details = get_video_details(video_id, api_key)
                if details:
                    self.title_label.setText(f"Title: {details['title']}")
                    self.author_label.setText(f"Author: {details['author']}")
                    response = requests.get(details['thumbnail'])
                    if response.status_code == 200:
                        image = QtGui.QImage()
                        image.loadFromData(response.content)
                        pixmap = QtGui.QPixmap(image)
                        self.thumbnail_label.setPixmap(
                            pixmap.scaled(self.thumbnail_label.size(), QtCore.Qt.KeepAspectRatio))
                    else:
                        self.thumbnail_label.clear()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Failed to retrieve video details")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Invalid YouTube URL")
        except Exception as e:
            print("Error in find_video" + e)


    def download_comments(self):
        video_url = self.url_input.text()
        video_id = self.extract_video_id(video_url)
        api_key = YOUTUBE_API
        if video_id:
            comments = get_video_comments(video_id, api_key)
            if comments:
                if not os.path.exists('comments'):
                    os.makedirs('comments')
                file_path = os.path.join('comments', video_id + ".txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    for comment in comments:
                        f.write(f"{comment['author']}: {comment['text']}\n")
                        for reply in comment['replies']:
                            f.write(f"  {reply['author']}: {reply['text']}\n")
                QtWidgets.QMessageBox.information(self, "Success", "Comments downloaded successfully")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to retrieve comments")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid YouTube URL")

    def extract_video_id(self, url):
        video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
        return video_id.group(1) if video_id else None
