from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QDesktopWidget, QTextEdit)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from pynput.keyboard import Key, Controller
import time
import os
import sys
import sqlite3
import attackcodes
import Resources
import psutil


db = sqlite3.connect('database.db')# database needs to be in directory
cur = db.cursor()

idnum = 0

class Login(QMainWindow):
    home_window = QtCore.pyqtSignal()

    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi("login.ui", self)
        self.signup_Button.clicked.connect(self.show_dialog_signup)
        self.signup_Button.clicked.connect(self.clear)
        self.login_Button.clicked.connect(self.show_dialog_login)
        self.login_Button.clicked.connect(self.clear)

    def clear(self):
        self.username.clear()
        self.password.clear()

    def show_dialog_signup(self):  #Displays a dialog for user
        dialog = uic.loadUi("dialog.ui")
        if self.check_if_exists(self.username.text()):
            dialog.placeHolder.setText("User Already Exists")
            ans = dialog.exec()

        else:
            if self.username.text()!= "":
                    if self.password.text()!= "":
                        dialog.placeHolder.setText("New User Created")
                        ans = dialog.exec()
                        if ans == 1:
                            self.create_new_user(self.username.text(), self.password.text())
                            self.home_window.emit()
                            self.close()
                    else:
                        dialog.placeHolder.setText("Please Enter Password")
                        ans = dialog.exec()
            else:
                dialog.placeHolder.setText("Please Enter Username")
                ans = dialog.exec()
                    
    def create_new_user(self, user, pwd):
        global idnum
        if idnum is not 0:
            cur.execute(""" INSERT INTO database (username, password, RFID) VALUES (?,?,?)""", (user, pwd ,idnum))
        else:    
            cur.execute(""" INSERT INTO database (username, password) VALUES (?,?)""", (user, pwd))
        db.commit()
        idnum = 0

    def check_if_exists(self, user): #Check in database.db if user is already in database

        result = None
        for row in cur.execute("SELECT * FROM database WHERE username=?", (user,)):  # Check in database if user exists
            result = row[1]

        if result is None:
            return 0
        else:
            return 1
        
    def login_check(self,user,pwd): #This function checks if user and password is in the database
        result = None
        for row in cur.execute("SELECT * FROM database WHERE (username=? AND password=?)", (user, pwd)):
            print(row[1])
            result = row[1]

        if result is None:
            return 0
        else:
            return 1
    
    def show_dialog_login(self):
        dialog = uic.loadUi("dialog.ui")
        if self.login_check(self.username.text(), self.password.text()):
            dialog.placeHolder.setText("Login Successful")
            ans = dialog.exec()
            if ans == 1:
                self.home_window.emit()
                self.close()

        else:
            dialog.placeHolder.setText("User or Password Incorrect")
            ans = dialog.exec()

class Home(QMainWindow):
    tutorial_window = QtCore.pyqtSignal()
    attacks_window = QtCore.pyqtSignal()
    videos_window = QtCore.pyqtSignal()
    monitor_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Home, self).__init__()
        uic.loadUi("Home.ui", self)
        self.Tutorial_Button.clicked.connect(self.Tutorials)
        self.Attacks_Button.clicked.connect(self.Attacks)
        self.Videos_Button.clicked.connect(self.Videos)
        self.Counter_Button.clicked.connect(self.Monitor)
    
    def Tutorials(self):
        self.tutorial_window.emit()
        self.close()
        
    def Attacks(self):
        self.attacks_window.emit()
        self.close()
        
    def Videos(self):
        self.videos_window.emit()
        self.close()
    
    def Monitor(self):
        self.monitor_window.emit()
    
class Tutorial(QMainWindow):
    vulnerabilities_window = QtCore.pyqtSignal()
    malware_window = QtCore.pyqtSignal()
    whatis_window = QtCore.pyqtSignal()
    counterinfo_window = QtCore.pyqtSignal()
    home_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Tutorial, self).__init__()
        uic.loadUi("Tutorial.ui", self)
        self.Vulnerability_Button.clicked.connect(self.Vulnerabilities)
        self.Malware_Button.clicked.connect(self.Malware)
        self.DDoS_Button.clicked.connect(self.whatis)
        self.Countermeasure_Button.clicked.connect(self.Counter)
        self.Back_Button.clicked.connect(self.Back)
        
    def Vulnerabilities(self):
        self.vulnerabilities_window.emit()
        self.close()   
        
    def Malware(self):
        self.malware_window.emit()
        self.close()
        
    def whatis(self):
        self.whatis_window.emit()
        self.close()
        
    def Counter(self):
        self.counterinfo_window.emit()
        self.close()
        
    def Back(self):
        self.home_window.emit()
        self.close()

class Vulnerabilities(QMainWindow):
    integrity_window = QtCore.pyqtSignal()
    confidentiality_window = QtCore.pyqtSignal()
    availability_window = QtCore.pyqtSignal()
    tutorial_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Vulnerabilities, self).__init__()
        uic.loadUi("Vulnerabilities.ui", self)
        self.Integrity_Button.clicked.connect(self.Integrity)
        self.Confidentiality_Button.clicked.connect(self.Confidentiality)
        self.Availability_Button.clicked.connect(self.Availability)
        self.Back_Button.clicked.connect(self.Back)
        
    def Integrity(self):
        self.integrity_window.emit()
        self.close()
    
    def Confidentiality(self):
        self.confidentiality_window.emit()
        self.close()
    
    def Availability(self):
        self.availability_window.emit()
        self.close()
    
    def Back(self):
        self.tutorial_window.emit()
        self.close()
    
class Integrity(QMainWindow):
    vulnerabilities_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Integrity, self).__init__()
        uic.loadUi("Integrity.ui", self)
        self.Back_Button.clicked.connect(self.Back)
    
    def Back(self):
        self.vulnerabilities_window.emit()
        self.close()
        
class Confidentiality(QMainWindow):
    vulnerabilities_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Confidentiality, self).__init__()
        uic.loadUi("Confidentiality.ui", self)
        self.Back_Button.clicked.connect(self.Back)
    
    def Back(self):
        self.vulnerabilities_window.emit()
        self.close()

class Availability(QMainWindow):
    vulnerabilities_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Availability, self).__init__()
        uic.loadUi("Availability.ui", self)
        self.Back_Button.clicked.connect(self.Back)
    
    def Back(self):
        self.vulnerabilities_window.emit()
        self.close()

class Malware(QMainWindow):
    tutorial_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Malware, self).__init__()
        uic.loadUi("Malware.ui", self)
        self.Back_Button.clicked.connect(self.Back)
    
    def Back(self):
        self.tutorial_window.emit()
        self.close()

class Whatis(QMainWindow):
    tutorial_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Whatis, self).__init__()
        uic.loadUi("Whatis.ui", self)
        self.Back_Button.clicked.connect(self.Back)
    
    def Back(self):
        self.tutorial_window.emit()
        self.close()
        
class CounterInfo(QMainWindow):
    tutorial_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(CounterInfo, self).__init__()
        uic.loadUi("CounterInfo.ui", self)
        self.Back_Button.clicked.connect(self.Back)
    
    def Back(self):
        self.tutorial_window.emit()
        self.close()
        
class Videos(QMainWindow):
    countervideo_window = QtCore.pyqtSignal()
    hackvideo_window = QtCore.pyqtSignal()
    home_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Videos, self).__init__()
        uic.loadUi("Videos.ui", self)
        self.Avideo_Button.clicked.connect(self.Avideo)
        self.Cvideo_Button.clicked.connect(self.Cvideo)
        self.Back_Button.clicked.connect(self.Back)
        
    def Avideo(self):
        self.hackvideo_window.emit()

    
    def Cvideo(self):
        self.countervideo_window.emit()
    
    def Back(self):
        self.home_window.emit()
        self.close()

class HackVideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(HackVideoWindow, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/home/pi/Desktop/DDosTest/AttackVideo.mov")))
        self.playButton.setEnabled(True)
        
        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


class CounterVideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(CounterVideoWindow, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/home/pi/Desktop/DDosTest/CM Demo vid.MOV")))
        self.playButton.setEnabled(True)
        
        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

class Attacks(QMainWindow):
    home_window = QtCore.pyqtSignal()

    def __init__(self):
        super(Attacks, self).__init__()
        uic.loadUi("Attacks.ui", self)
        self.Infect_Button.clicked.connect(self.Infect)
        self.Attack_Button.clicked.connect(self.Attack)
        self.Back_Button.clicked.connect(self.Back)
        
    def Back(self):
        self.home_window.emit()
        self.close()
        
    def Infect(self):
        attackcodes.infect()
        
        
    def Attack(self):
        print("attack")
        
class Monitor(QMainWindow):
    warning_window = QtCore.pyqtSignal()

    def __init__(self):
        super(Monitor, self).__init__()
        uic.loadUi("attackMon.ui", self)
        self.bothPer.clicked.connect(self.Both)
        self.cpuPer.clicked.connect(self.Cpu)
        self.ramPer.clicked.connect(self.Ram)
        
    def Both(self):
        while True:
            cpu = psutil.cpu_percent(interval = 1)
            memory = psutil.virtual_memory()[2]
            print('CPU usage %: ',cpu)
            print('RAM memory usage %: ',memory)
            if cpu > 99:
                #print("CPU percentage load too high!")
                self.warning_window.emit()
                
            elif memory > 68:
                self.warning_window.emit()
        
    def Cpu(self):
        while True:
            cpu = psutil.cpu_percent(interval = 1)
            print('CPU usage %: ',cpu)
            if cpu > 99  :
                self.warning_window.emit()
        
        
    def Ram(self):
        while True:
            memory = psutil.virtual_memory()[2]
            time.sleep(1)
            print('RAM memory usage %: ',memory)
            if memory > 68:
                self.warning_window.emit()
                
class warning(QMainWindow):

    def __init__(self):
        super(warning, self).__init__()
        uic.loadUi("Mess.ui", self)
            
class Controller():

    def __init__(self):
        pass
    
    def show_Login(self):
        self.login = Login()
        self.login.home_window.connect(self.show_Home)
        self.login.show()
        
    def show_Home(self):
        self.home = Home()
        self.home.tutorial_window.connect(self.show_tutorial)
        self.home.attacks_window.connect(self.show_attacks)
        self.home.videos_window.connect(self.show_videos)
        self.home.monitor_window.connect(self.show_monitor)
        self.home.show()
        
    def show_tutorial(self):
        self.tutorial = Tutorial()
        self.tutorial.vulnerabilities_window.connect(self.show_vulnerabilities)
        self.tutorial.malware_window.connect(self.show_malware)
        self.tutorial.whatis_window.connect(self.show_whatis)
        self.tutorial.home_window.connect(self.show_Home)
        self.tutorial.counterinfo_window.connect(self.show_counterinfo)
        self.tutorial.show()
    
    def show_vulnerabilities(self):
        self.vulnerabilities = Vulnerabilities()
        self.vulnerabilities.integrity_window.connect(self.show_integrity)
        self.vulnerabilities.confidentiality_window.connect(self.show_confidentiality)
        self.vulnerabilities.availability_window.connect(self.show_availability)
        self.vulnerabilities.tutorial_window.connect(self.show_tutorial)
        self.vulnerabilities.show()
    
    def show_integrity(self):
        self.integrity = Integrity()
        self.integrity.vulnerabilities_window.connect(self.show_vulnerabilities)
        self.integrity.show()
    
    def show_confidentiality(self):
        self.confidentiality = Confidentiality()
        self.confidentiality.vulnerabilities_window.connect(self.show_vulnerabilities)
        self.confidentiality.show()
        
    def show_availability(self):
        self.availability = Availability()
        self.availability.vulnerabilities_window.connect(self.show_vulnerabilities)
        self.availability.show()
    
    def show_malware(self):
        self.malware = Malware()
        self.malware.tutorial_window.connect(self.show_tutorial)
        self.malware.show()
    
    def show_whatis(self):
        self.whatis = Whatis()
        self.whatis.tutorial_window.connect(self.show_tutorial)
        self.whatis.show()
    
    def show_counterinfo(self):
        self.counterinfo = CounterInfo()
        self.counterinfo.tutorial_window.connect(self.show_tutorial)
        self.counterinfo.show()
    
    def show_videos(self):
        self.videos = Videos()
        self.videos.home_window.connect(self.show_Home)
        self.videos.hackvideo_window.connect(self.show_hackvideo)
        self.videos.countervideo_window.connect(self.show_countervideo)
        self.videos.show()
    
    def show_hackvideo(self):
        self.hackvideo = HackVideoWindow()
        self.hackvideo.show()
    
    def show_countervideo(self):
        self.countervideo = CounterVideoWindow()
        self.countervideo.show()
    
    def show_attacks(self):
        self.attacks= Attacks()
        self.attacks.home_window.connect(self.show_Home)
        self.attacks.show()
    
    def show_monitor(self):
        self.monitor= Monitor()
        self.monitor.warning_window.connect(self.show_warning)
        self.monitor.show()
        
    def show_warning(self):
        self.warning = warning()
        self.warning.show()
   
    
app = QtWidgets.QApplication(sys.argv)
window = Controller()
window.show_Login()
app.exec_()

   
   