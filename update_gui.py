from PyQt5 import QtCore, QtGui, QtWidgets
from youtubesearchpython import Playlist
import json, os, pafy, requests, math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND = os.path.join(os.path.join(BASE_DIR, 'icons'), 'background.png')
DRIVER = os.path.join(os.path.join(BASE_DIR, 'Driver'), 'chromedriver.exe')

class Ui_MainWindow(object):
        def returnVideoURL(self, video_title):
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
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(740, 600)
                font = QtGui.QFont()
                font.setFamily("Nirmala UI")
                font.setPointSize(5)
                MainWindow.setFont(font)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(BACKGROUND), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                MainWindow.setWindowIcon(icon)
                MainWindow.setStyleSheet("background: #333;")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.label = QtWidgets.QLabel(self.centralwidget)
                self.label.setGeometry(QtCore.QRect(0, 0, 715, 151))
                font = QtGui.QFont()
                font.setFamily("Origin Tech Demo")
                font.setPointSize(22)
                self.label.setFont(font)
                self.label.setStyleSheet("color: rgb(82, 91, 255);")
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("label")
                self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
                self.lineEdit.setGeometry(QtCore.QRect(130, 170, 481, 41))
                font = QtGui.QFont()
                font.setFamily("Nirmala UI")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                font.setStrikeOut(False)
                self.lineEdit.setFont(font)
                self.lineEdit.setStyleSheet("QLineEdit{\n"
        "background: #f3f3f3;\n"
        "color: #333;\n"
        "border: 2px solid rgb(85, 85, 255);\n"
        "border-radius: 10px;\n"
        "padding:10px;\n"
        "}")
                self.lineEdit.setObjectName("lineEdit")
                self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
                self.progressBar.setGeometry(QtCore.QRect(130, 297, 481, 17))
                font = QtGui.QFont()
                font.setPointSize(8)
                self.progressBar.setFont(font)
                self.progressBar.setStyleSheet("QProgressBar\n"
        "{\n"
        "border-radius: 10px;\n"
        "background: white;\n"
        "color: #fff;\n"
        "}\n"
        "QProgressBar::chunk \n"
        "{\n"
        "background-color: #05B8CC;\n"
        "border-radius :10px;\n"
        "}      ")
                self.progressBar.setProperty("value", 0)
                self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
                self.progressBar.setObjectName("progressBar")
                self.progressBar.setMinimum(0)
                self.progressBar.setMaximum(100)
                self.label_2 = QtWidgets.QLabel(self.centralwidget)
                self.label_2.setGeometry(QtCore.QRect(130, 220, 481, 61))
                self.label_2.setWordWrap(True)
                font = QtGui.QFont()
                font.setFamily("Nirmala UI")
                font.setPointSize(8)
                font.setBold(True)
                font.setWeight(75)
                self.label_2.setFont(font)
                self.label_2.setStyleSheet("padding: 10px;\n"
        "color: white;\n"
        "border-radius: 10px;")
                self.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_2.setObjectName("label_2")
                self.pushButton = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton.setGeometry(QtCore.QRect(130, 340, 481, 41))
                font = QtGui.QFont()
                font.setFamily("Nirmala UI")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.pushButton.setFont(font)
                self.pushButton.setStyleSheet("QPushButton{\n"
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
                self.pushButton.setObjectName("pushButton")
                MainWindow.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)
                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
                self.pushButton.clicked.connect(self.start_collecting)
        def progressing(self, data):
                percent = math.floor((data[0]/data[1]) * 100)
                self.progressBar.setValue(percent)
                self.update_info("Collecting {}".format(data[2]))
        def completed(self, data):
                self.update_info("""
                Total Media {} Total Fetched {}
                Total Failed {}
                """.format(data[0], data[1], data[2]))
                self.pushButton.setEnabled(True)
                self.progressBar.setValue(100)
        def start_collecting(self):
                self.update_info('Collecting data\nDo not close the window')
                self.progressBar.setValue(0)
                query = self.lineEdit.text()
                self.lineEdit.setText("")
                link = 'none'
                if query != '':
                        self.pushButton.setEnabled(False)
                        if query.startswith('https://www.youtube.com/watch'):
                                url = query
                        elif query.startswith("https://www.youtube.com/playlist"):
                                self.downloadingThread = MediaCollector()
                                self.downloadingThread.start()
                                self.downloadingThread.progressEvent.connect(self.progressing)
                                self.downloadingThread.completeEvent.connect(self.completed)
                                self.downloadingThread.messageEvent.connect(self.message)
                                global videoListUrl
                                videoListUrl = query
                                link = 'list'
                        else:
                                url = self.returnVideoURL(query)
                        if link == 'none':
                                filepath = os.path.join(BASE_DIR, 'playlist.url.json')
                                file = open(filepath, 'r+')
                                urllist = json.load(file)['urls']
                                video_title = pafy.new(url).getbestaudio().title
                                urllist.append(url)
                                newUrl = list(set(urllist))
                                file.seek(0)
                                file.truncate()
                                data = {
                                        "urls": newUrl
                                }
                                json.dump(data, file, indent=4)
                                self.progressBar.setValue(100)
                                self.update_info("Media {} has been added to Playlist".format(video_title))
                                self.pushButton.setEnabled(True)
        def message(self, text):
                self.update_info(text)
        def update_info(self, text):
                self.label_2.setText(self._translate("MainWindow", text))
        def retranslateUi(self, MainWindow):
                self._translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(self._translate("MainWindow", "Update Library"))
                self.label.setText(self._translate("MainWindow", "Update Media Playlist"))
                self.lineEdit.setPlaceholderText(self._translate("MainWindow", "Video url or video title"))
                self.label_2.setText(self._translate("MainWindow", "Progress Information will be shown here"))
                self.pushButton.setText(self._translate("MainWindow", "Update"))
class MediaCollector(QtCore.QThread):
        completeEvent = QtCore.pyqtSignal(list)
        progressEvent = QtCore.pyqtSignal(list)
        messageEvent = QtCore.pyqtSignal(str)
        def run(self):
                self.messageEvent.emit('Collecting Playable URLS')                
                with open(os.path.join(BASE_DIR, 'playlist.url.json'), 'r+') as jfile:
                        previousList = list(json.load(jfile))
                        if len(previousList) > 0:
                                previousList = previousList['urls']
                        else:
                                previousList = []
                        playlist = Playlist(videoListUrl)
                        while playlist.hasMoreVideos:
                                playlist.getNextVideos()
                        jfile.seek(0)
                        jfile.truncate()
                        finalList = [videos['link'] for videos in playlist.videos]
                        newList = previousList + finalList
                        self.progressEvent.emit([len(finalList), len(finalList), playlist.info['info']['title']])
                        data = {
                                "urls": list(newList)
                        }
                        json.dump(data, jfile, indent=4)
                        
                        self.completeEvent.emit([int(playlist.info['info']['videoCount']), len(playlist.videos), int(playlist.info['info']['videoCount']) - int(len(playlist.videos))])