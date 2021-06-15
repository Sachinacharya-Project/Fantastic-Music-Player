from logging import currentframe
from PyQt5 import QtCore, QtGui, QtWidgets
from vlc import MediaPlayer
import json, pafy, os, requests
from update_gui import Ui_MainWindow as SecondScr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'icons')

VOLUME_UP = os.path.join(ICON_DIR, 'volume-up-solid.svg')
VOLUME_DOWN = os.path.join(ICON_DIR, 'volume-down-solid.svg')
STOP = os.path.join(ICON_DIR, 'stop-solid.svg')
PLAY = os.path.join(ICON_DIR, 'play-solid.svg')
PAUSE = os.path.join(ICON_DIR, 'pause-solid.svg')
UPDATE = os.path.join(ICON_DIR, 'marker-solid.svg')
NEXT = os.path.join(ICON_DIR, 'arrow-right-solid.svg')
PREVIOUS = os.path.join(ICON_DIR, 'arrow-left-solid.svg')
MUTE = os.path.join(ICON_DIR, 'volume-mute-solid.svg')
BACKGROUND = os.path.join(ICON_DIR, 'background.png')

def returnVideoURL(video_title):
        url = 'https://www.youtube.com/results?q=' + video_title
        count = 0
        cont = requests.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
                count+=1
                if i == 'WEB_PAGE_TYPE_WATCH':
                        break
        if lst[count-5] == "/results":
                raise Exception("No video found.")
        return "https://www.youtube.com"+lst[count-5]
class Ui_MainWindow(object):
        def default(self, current_video_index=0):
                self.shouldReload = False
                self.collected_volume = 100
                if self.collect_urls():
                        self.current_video_index = current_video_index
                        self.current_url = self.urllist[self.current_video_index]
                        self.metadata = pafy.new(self.current_url)
                        self.current_playable_url = self.metadata.getbestaudio().url
                        self.video_title = self.metadata.title
                        self.music_titles.setText(self._translate("MainWindow", "Selected Media {}".format(self.video_title)))
                        self.player = MediaPlayer(self.current_playable_url)
                        self.update_info("Please do not use loop, repeat and close on end features")
                else:
                        self.shouldReload = True
        def uncheckElse(self, state):
                if state == QtCore.Qt.Checked:
                        if self.tool_window.sender() == self.loop:
                                self.closeEnd.setChecked(False)
                                self.repeat.setChecked(False)
                                if self.lastThreadName != 'loop':
                                        if self.lastThreadName == 'closeEnd':
                                                self.closeEndThread.stop()
                                        else:
                                                self.repeatThread.stop()
                                        self.loopThread.start()
                                        self.lastThreadName = 'loop'
                        elif self.tool_window.sender() == self.repeat:
                                self.closeEnd.setChecked(False)
                                self.loop.setChecked(False)
                                if self.lastThreadName != 'repeat':
                                        if self.lastThreadName == 'closeEnd':
                                                self.closeEndThread.stop()
                                        else:
                                                self.loopThread.stop()
                                        self.repeatThread.start()
                                        self.lastThreadName = 'repeatThread'
                        else:
                                self.repeat.setChecked(False)
                                self.loop.setChecked(False)
                                if self.lastThreadName != 'closeEnd':
                                        if self.lastThreadName == 'loop':
                                                self.loopThread.stop()
                                        else:
                                                self.repeatThread.stop()
                                        self.closeEndThread.start()
                                        self.lastThreadName = 'closeEnd'
                else:
                        if self.tool_window.sender() == self.repeat:
                                self.repeatThread.stop()
                        elif self.tool_window.sender() == self.loop:
                                self.loopThread.stop()
                        else:
                                self.closeEndThread.stop()
        def progressHandle(self, current_pos):
                current_maximum_val = self.seek_bar.maximum()
                playermax = self.player.get_length()
                if current_maximum_val != playermax:
                        self.seek_bar.setMaximum(int(playermax))
                self.seek_bar.setValue(current_pos)
        def playPauseHandle(self):
                if self.shouldReload:
                        self.default()
                        self.playPauseHandle()
                else:
                        if self.player.is_playing() == 0:
                                self.player.play()
                                self.music_titles.setText(self._translate("MainWindow", "Now Playing {}".format(self.video_title)))
                                self.update_info("Playing Media")
                                self.mediaLength = self.player.get_length()
                                self.seek_bar.setMaximum(self.mediaLength)
                                icon_url = PAUSE
                                self.workThread = ProgressBarThread(self.player, self.seek_bar)
                                self.workThread.start()
                                self.workThread.progressing.connect(self.progressHandle)
                        else:
                                self.player.pause()
                                self.music_titles.setText(self._translate("MainWindow", "Now Playing {} paused".format(self.video_title)))
                                self.update_info("Paused Media")
                                icon_url = PLAY
                                self.workThread.stop()
                        self.setPlayButtonIcon(icon_url)
        def setPlayButtonIcon(self, url):
                self.icon1.addPixmap(QtGui.QPixmap(url), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.playPause.setIcon(self.icon1)
                self.playPause.setIconSize(QtCore.QSize(20, 20))
        def update_info(self, message):
                self.info.setText(self._translate("MainWindow", message))
        def stopMediaHandle(self):
                if self.player.is_playing() == 1:
                        before_vol = int(self.player.audio_get_volume())
                        self.player.stop()
                        self.update_info('Stopped Media')
                        icon_url = PLAY
                        self.setPlayButtonIcon(icon_url)
                        self.player.audio_set_volume(before_vol)
                        self.seek_bar.setValue(0)
        def download_media_callback(self, *args):
                self.update_info("Media {} Downloaded Successfull".format(self.video_title))
        def download_media(self):
                direc = os.path.join(BASE_DIR, 'Downloads')
                if os.path.exists(direc) == False:
                        os.mkdir(direc)
                self.update_info('Downloading {}'.format(self.video_title))
                thebestmedia = self.metadata.getbestaudio()
                thebestmedia.download(os.path.join(direc, f"{self.video_title}.{thebestmedia.extension}"), quiet=True)
                self.download_media_callback()
        def volumeControl(self, dats):
                status = self.player.audio_get_mute()
                if dats == 'down':
                        vol = int(self.player.audio_get_volume()) - 3
                        if vol <= 0:
                                vol = 0
                                if self.player.audio_get_mute() == 0:
                                        self.muteUnMuteHandle("")
                        else:
                                vol = vol
                                self.player.audio_set_volume(vol)
                                current_volume = self.player.audio_get_volume()
                                self.update_info("Current Volume {}(Down 3)".format(current_volume))
                                self.volume.setValue(vol)
                elif dats == 'slider':
                        val = self.player.audio_get_volume()
                        current_value = self.volume.value()
                        self.player.audio_set_volume(current_value)
                        self.update_info("Current Volume {}(Changed {})".format(current_value, val))
                        status = self.player.audio_get_mute()
                        if current_value == 0:
                                if status == 0:
                                        self.muteUnMuteHandle()
                        else:
                                if status == 1:
                                        self.muteUnMuteHandle()
                else:
                        if status == 1:
                                self.collected_volume = 3
                                self.muteUnMuteHandle()
                        else:
                                vol = int(self.player.audio_get_volume()) + 3
                                if vol > 100:
                                        vol = 100
                                else:
                                        vol = vol
                                current_volume = self.player.audio_get_volume()
                                self.update_info("Current Volume {}(Up 3)".format(current_volume))
                                self.player.audio_set_volume(vol)
                                self.volume.setValue(vol)
        def playPrevious(self):
                self.stopMediaHandle()
                nextIndex = self.current_video_index - 1
                if nextIndex < 0:
                        self.current_video_index = len(self.urllist) - 1
                else:
                        self.current_video_index = nextIndex
                self.default(self.current_video_index)
                self.playPauseHandle()
        def playNext(self):
                self.stopMediaHandle()
                nextIndex = self.current_video_index + 1
                if nextIndex >= len(self.urllist):
                        self.current_video_index = 0
                else:
                        self.current_video_index = nextIndex
                self.default(self.current_video_index)
                self.playPauseHandle()
        def createNewWindows(self):
                self.Second = QtWidgets.QMainWindow()
                self.second_ui = SecondScr()
                self.second_ui.setupUi(self.Second)
                self.Second.show()
        def muteUnMuteHandle(self, hand=""):
                status = self.player.audio_get_mute()
                self.player.audio_toggle_mute()
                if status == 0:
                        self.collected_volume = int(self.player.audio_get_volume())
                        self.volume.setValue(0)
                        self.mute.setStyleSheet("QPushButton{\n"
        "background-color: #333;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "")
                else:
                        self.volume.setValue(self.collected_volume)
                        self.mute.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "")
        def collect_urls(self):
                self.jsonDir = os.path.join(BASE_DIR, 'playlist.url.json')
                self.urllist_file = open(self.jsonDir, 'r+')
                self.urllist = json.load(self.urllist_file)['urls']
                if len(self.urllist) == 0:
                        self.music_titles.setText(self._translate("MainWindow", "No Media Url is found in the playlist"))
                        self.update_info('Please Populate by clicking update')
                        return False
                else:
                        return True
        def setupUi(self, MainWindow):
                self.lastThreadName = ''
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(800, 600)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
                MainWindow.setSizePolicy(sizePolicy)
                MainWindow.setMinimumSize(QtCore.QSize(0, 0))
                MainWindow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(BACKGROUND), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                MainWindow.setWindowIcon(icon)
                MainWindow.setStyleSheet("background: #222;")
                MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                self.tool_window = MainWindow
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.window_title = QtWidgets.QLabel(self.centralwidget)
                self.window_title.setGeometry(QtCore.QRect(10, 0, 781, 141))
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.window_title.sizePolicy().hasHeightForWidth())
                self.window_title.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setFamily("Origin Tech Demo")
                font.setPointSize(22)
                font.setBold(True)
                font.setWeight(75)
                self.window_title.setFont(font)
                self.window_title.setStyleSheet("color: rgb(82, 91, 255);")
                self.window_title.setAlignment(QtCore.Qt.AlignCenter)
                self.window_title.setObjectName("window_title")
                self.music_titles = QtWidgets.QLabel(self.centralwidget)
                self.music_titles.setGeometry(QtCore.QRect(10, 150, 781, 51))
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                self.music_titles.setFont(font)
                self.music_titles.setStyleSheet("color: rgb(82, 91, 255);padding: 10px;font-weight: bold;")
                self.music_titles.setAlignment(QtCore.Qt.AlignCenter)
                self.music_titles.setObjectName("music_titles")
                self.playPause = QtWidgets.QPushButton(self.centralwidget)
                self.playPause.setGeometry(QtCore.QRect(330, 347, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                self.threadList = []
                self.playPause.setFont(font)
                self.playPause.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}")
                self.playPause.setText("")
                self.icon1 = QtGui.QIcon()
                self.icon1.addPixmap(QtGui.QPixmap(PLAY), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.playPause.setIcon(self.icon1)
                self.playPause.setIconSize(QtCore.QSize(20, 20))
                self.playPause.setObjectName("playPause")
                self.playPause.clicked.connect(self.playPauseHandle)
                self.next_btn = QtWidgets.QPushButton(self.centralwidget)
                self.next_btn.setGeometry(QtCore.QRect(500, 347, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(11)
                self.next_btn.setFont(font)
                self.next_btn.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}")
                self.next_btn.setText("")
                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap(NEXT), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.next_btn.setIcon(icon2)
                self.next_btn.setIconSize(QtCore.QSize(20, 20))
                self.next_btn.setObjectName("next_btn")
                self.next_btn.clicked.connect(self.playNext)
                self.previous_btn = QtWidgets.QPushButton(self.centralwidget)
                self.previous_btn.setGeometry(QtCore.QRect(160, 347, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(11)
                self.previous_btn.setFont(font)
                self.previous_btn.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}")
                self.previous_btn.setText("")
                icon3 = QtGui.QIcon()
                icon3.addPixmap(QtGui.QPixmap(PREVIOUS), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.previous_btn.setIcon(icon3)
                self.previous_btn.setIconSize(QtCore.QSize(20, 20))
                self.previous_btn.setObjectName("previous_btn")
                self.previous_btn.clicked.connect(self.playPrevious)
                self.volume_down = QtWidgets.QPushButton(self.centralwidget)
                self.volume_down.setGeometry(QtCore.QRect(160, 430, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(11)
                self.volume_down.setFont(font)
                self.volume_down.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}")
                self.volume_down.setText("")
                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap(VOLUME_DOWN), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.volume_down.setIcon(icon4)
                self.volume_down.setIconSize(QtCore.QSize(20, 20))
                self.volume_down.setObjectName("volume_down")
                self.volume_down.clicked.connect(lambda: self.volumeControl('down'))
                self.volume_up = QtWidgets.QPushButton(self.centralwidget)
                self.volume_up.setGeometry(QtCore.QRect(500, 430, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(11)
                self.volume_up.setFont(font)
                self.volume_up.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "")
                self.volume_up.setText("")
                icon5 = QtGui.QIcon()
                icon5.addPixmap(QtGui.QPixmap(VOLUME_UP), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.volume_up.setIcon(icon5)
                self.volume_up.setIconSize(QtCore.QSize(20, 20))
                self.volume_up.setObjectName("volume_up")
                self.volume_up.clicked.connect(lambda: self.volumeControl('up'))
                self.volume = QtWidgets.QSlider(self.centralwidget)
                self.volume.setGeometry(QtCore.QRect(670, 340, 22, 211))
                self.volume.setStyleSheet("QSlider::groove:horizontal { \n"
        "    background-color: white;\n"
        "    border: 0px solid #424242;\n"
        "    height: 4px;\n"
        "    border-radius: 4px;\n"
        "}\n"
        "QSlider::handle:horizontal { \n"
        "    background-color: rgb(82, 91, 255);\n"
        "    border: 2px solid rgb(82, 91, 255); \n"
        "    width: 3px; \n"
        "    height: 2px; \n"
        "    line-height: 2px; \n"
        "    margin-top: -5px; \n"
        "    margin-bottom: -5px; \n"
        "    border-radius: 3px; \n"
        "}\n"
        "QSlider::handle:horizontal:hover { \n"
        "    border-radius: 3px;\n"
        "}")
                self.volume.setMaximum(100)
                self.volume.setMinimum(0)
                self.volume.setProperty("value", 100)
                self.volume.setOrientation(QtCore.Qt.Vertical)
                self.volume.setObjectName("volume")
                self.volume.valueChanged.connect(lambda: self.volumeControl('slider'))
                self.seek_bar = QtWidgets.QSlider(self.centralwidget)
                self.seek_bar.setGeometry(QtCore.QRect(20, 240, 751, 22))
                self.seek_bar.setMouseTracking(True)
                self.seek_bar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.seek_bar.setStyleSheet("QSlider::groove:horizontal { \n"
        "    background-color: white;\n"
        "    border: 0px solid #424242;\n"
        "    height: 4px;\n"
        "    border-radius: 4px;\n"
        "}\n"
        "QSlider::handle:horizontal { \n"
        "    background-color: rgb(82, 91, 255);\n"
        "    border: 2px solid rgb(82, 91, 255); \n"
        "    width: 3px; \n"
        "    height: 2px; \n"
        "    line-height: 2px; \n"
        "    margin-top: -5px; \n"
        "    margin-bottom: -5px; \n"
        "    border-radius: 3px; \n"
        "}\n"
        "QSlider::handle:horizontal:hover { \n"
        "    border-radius: 3px;\n"
        "}")
                self.seek_bar.setMaximum(100)
                self.seek_bar.setProperty("value", 0)
                self.seek_bar.setOrientation(QtCore.Qt.Horizontal)
                self.seek_bar.setObjectName("seek_bar")
                self.info = QtWidgets.QLabel(self.centralwidget)
                self.info.setGeometry(QtCore.QRect(0, 190, 791, 41))
                self.info.setStyleSheet("color: rgb(82, 91, 255);")
                self.info.setAlignment(QtCore.Qt.AlignCenter)
                self.info.setObjectName("info")
                self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
                self.stop_btn.setGeometry(QtCore.QRect(330, 430, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(11)
                self.stop_btn.setFont(font)
                self.stop_btn.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}")
                self.stop_btn.setText("")
                icon6 = QtGui.QIcon()
                icon6.addPixmap(QtGui.QPixmap(STOP), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.stop_btn.setIcon(icon6)
                self.stop_btn.setIconSize(QtCore.QSize(20, 20))
                self.stop_btn.setObjectName("stop_btn")
                self.stop_btn.clicked.connect(self.stopMediaHandle)
                self.loop = QtWidgets.QCheckBox(self.centralwidget)
                self.loop.setGeometry(QtCore.QRect(160, 290, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.loop.setFont(font)
                self.loop.setStyleSheet("QCheckBox{\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QCheckBox::checked{\n"
        "color: rgb(82, 91, 255);\n"
        "}")
                self.loop.setObjectName("loop")
                self.closeEnd = QtWidgets.QCheckBox(self.centralwidget)
                self.closeEnd.setGeometry(QtCore.QRect(500, 290, 151, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.closeEnd.setFont(font)
                self.closeEnd.setStyleSheet("QCheckBox{\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QCheckBox::checked{\n"
        "color: rgb(82, 91, 255);\n"
        "}\n"
        "")
                self.closeEnd.setObjectName("closeEnd")
                self.repeat = QtWidgets.QCheckBox(self.centralwidget)
                self.repeat.setGeometry(QtCore.QRect(330, 290, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.repeat.setFont(font)
                self.repeat.setStyleSheet("QCheckBox{\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QCheckBox::checked{\n"
        "color: rgb(82, 91, 255);\n"
        "}")
                self.repeat.setObjectName("repeat")

                self.loop.stateChanged.connect(self.uncheckElse)
                self.repeat.stateChanged.connect(self.uncheckElse)
                self.closeEnd.stateChanged.connect(self.uncheckElse)

                self.update = QtWidgets.QPushButton(self.centralwidget)
                self.update.setGeometry(QtCore.QRect(160, 510, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.update.setFont(font)
                self.update.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "")
                icon7 = QtGui.QIcon()
                icon7.addPixmap(QtGui.QPixmap(UPDATE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.update.setIcon(icon7)
                self.update.setObjectName("update")
                self.update.clicked.connect(self.createNewWindows)
                self.mute = QtWidgets.QPushButton(self.centralwidget)
                self.mute.setGeometry(QtCore.QRect(500, 510, 141, 41))
                self.mute.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "")
                self.mute.setText("")
                self.icon8 = QtGui.QIcon()
                self.icon8.addPixmap(QtGui.QPixmap(MUTE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.mute.setIcon(self.icon8)
                self.mute.setIconSize(QtCore.QSize(20, 20))
                self.mute.setObjectName("mute")
                self.mute.clicked.connect(lambda:self.muteUnMuteHandle('set'))
                self.download = QtWidgets.QPushButton(self.centralwidget)
                self.download.setGeometry(QtCore.QRect(330, 510, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.download.setFont(font)
                self.download.setStyleSheet("QPushButton{\n"
        "background-color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "QPushButton::pressed{\n"
        "background-color: rgb(82, 91, 255);\n"
        "font-weight: bold;\n"
        "color: white;\n"
        "padding: 10px;\n"
        "border-radius: 10px;\n"
        "}\n"
        "\n"
        "")
                self.download.setObjectName("download")
                self.download.clicked.connect(self.download_media)

                self.mediaLength = 0
                self.seek_bar.setValue(self.mediaLength)
                self.seek_bar.valueChanged.connect(self.valueIsChangedDetection)
                # Area Shortcuts
                self.play_pause_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('Space'), MainWindow)
                self.play_pause_shortcuts.activated.connect(self.playPauseHandle)
                
                self.next_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('Left'), MainWindow)
                self.next_shortcuts.activated.connect(lambda: self.skipTime('next'))
                
                self.previous_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('Right'), MainWindow)
                self.previous_shortcuts.activated.connect(lambda: self.skipTime('prev'))

                self.volumeUp_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('Up'), MainWindow)
                self.volumeUp_shortcuts.activated.connect(lambda: self.volumeControl('up'))

                self.volumeDown_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('Down'), MainWindow)
                self.volumeDown_shortcuts.activated.connect(lambda: self.volumeControl('down'))

                self.mute_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('M'), MainWindow)
                self.mute_shortcuts.activated.connect(self.muteUnMuteHandle)

                self.stop_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('S'), MainWindow)
                self.stop_shortcuts.activated.connect(self.stopMediaHandle)

                self.mute_shortcuts = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+D'), MainWindow)
                self.mute_shortcuts.activated.connect(self.download_media)

                # Threads
                flagis = QtCore.Qt.WindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
                MainWindow.setWindowFlags(flagis)
                MainWindow.setCentralWidget(self.centralwidget)
                self.retranslateUi(MainWindow)

                self.loopThread = loopThread(self.player)
                self.loopThread.videoEndedEvent.connect(self.changeNextVideo)
                self.repeatThread = repeatThread(self.player)
                self.closeEndThread = closeEndThread(self.player)
                MainWindow.customContextMenuRequested.connect(self.contextMenuEvent)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
        def skipTime(self, value):
                current_video_time = self.player.get_time()
                if value == 'prev':
                        video_length = self.player.get_length()
                        new_video_time = current_video_time + 5000
                        if new_video_time > video_length:
                                new_video_time = video_length - 1000
                else:
                        new_video_time = current_video_time - 5000
                        if new_video_time < 0:
                                new_video_time = 0
                self.update_info('Playing at {}/{} MS'.format(new_video_time, video_length))
                self.player.set_time(int(new_video_time))
        def pauseMediaForAWhile(self):
                self.player.pause()
        def valueIsChangedDetection(self):
                if not self.player.is_playing():
                        current_time = self.seek_bar.value()
                        self.player.set_time(int(current_time))
        def changeNextVideo(self, index):
                if index == 1:
                        self.playNext()
        def contextMenuEvent(self, position):
                contextMenu = QtWidgets.QMenu(MainWindow)
                contextMenu.setStyleSheet("QMenu{\n"
                "border-radius: 10px;\n"
                "background-color: #333;\n"
                "width: 250px;\n"
                "color: white;\n"
                "border: 0px solid white;\n"
                "padding: 10px;\n"
                "}\n"
                "QMenu:pressed{\n"
                "color: red;\n"
                "}\n")
                showPlaylist = contextMenu.addAction('Show Playlist')
                action = contextMenu.exec_(self.tool_window.mapToGlobal(position))
                if action == showPlaylist:
                        print('Showing Playlist')
        def retranslateUi(self, MainWindow):
                self._translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(self._translate("MainWindow", "Fantastic Music Player"))
                self.window_title.setText(self._translate("MainWindow", "Fantastic Music Player"))
                self.music_titles.setText(self._translate("MainWindow", "1. Falling by harry styles"))
                self.info.setText(self._translate("MainWindow", "Looping"))
                self.loop.setText(self._translate("MainWindow", "Loop"))
                self.closeEnd.setText(self._translate("MainWindow", "Close on finished"))
                self.repeat.setText(self._translate("MainWindow", "Repeat"))
                self.update.setText(self._translate("MainWindow", "Update"))
                self.download.setText(self._translate("MainWindow", "Download"))
                self.default()
class loopThread(QtCore.QThread):
        videoEndedEvent = QtCore.pyqtSignal(int)
        def __init__(self, player,parent=None):
            super().__init__(parent=parent)
            self.player = player
        def run(self):
                while 1:
                        if self.player.is_playing() == 1:
                                pass
                        else:
                                if str(self.player.get_state()) == 'State.Stopped':
                                        self.videoEndedEvent.emit(1)
        def stop(self):
                print('Ending Loop')
                self.isRunning = False
                self.terminate()
class repeatThread(QtCore.QThread):
        def __init__(self, player,parent=None):
            super().__init__(parent=parent)
            self.player = player
        def run(self):
                print('Repeating')
        def stop(self):
                print("Ending Repeating")
                self.isRunning = False
                self.terminate()
class closeEndThread(QtCore.QThread):
        def __init__(self, player,parent=None):
            super().__init__(parent=parent)
            self.player = player
        def run(self):
                print('Closing')
        def stop(self):
                print('Ending Closing')
                self.isRunning = False
                self.terminate()
class ProgressBarThread(QtCore.QThread):
        progressing = QtCore.pyqtSignal(int)
        def __init__(self, player, seekbar,parent=None):
                super().__init__(parent=parent)
                self.player = player
                self.seekbar = seekbar
        def run(self):
                self.seekbar.setMinimum(0)
                while 1:
                        while self.player.is_playing():
                                current_time = self.player.get_time()
                                total_length = self.player.get_length()
                                max_val = self.seekbar.maximum()
                                if int(total_length != max_val):
                                        self.seekbar.setMaximum(total_length)
                                if current_time >= 0:
                                        self.seekbar.setValue(current_time)
        def stop(self):
                self.isRunning = False
                self.terminate()

if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())