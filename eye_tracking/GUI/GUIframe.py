import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QToolTip, \
    QLabel, QSplitter, QTextEdit, QStackedWidget, QFormLayout, QLineEdit, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from qtconsole.qt import QtGui

import database_func

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.quit_sig = False
        self.initUI()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.currentStack = 1
        self.start = False

    def initUI(self):
        self.setWindowTitle('Eye Tracking')
        self.setWindowIcon(QIcon('eye.png'))

        self.start_btn = QPushButton('Start', self)
        self.start_btn.setCheckable(True)
        self.start_btn.toggled.connect(self.start_end)

        #setting button
        self.setting = QPushButton('Setting', self)
        self.setting.setCheckable(True)
        self.setting.toggled.connect(self.set_ip)
        self.setting.move(50, 0)

        self.ip_guide = QLabel('current IP Address : ' + database_func.host)
        #self.ip_guide = QLabel('current IP Address : ')
        self.ip_guide.setFont(QtGui.QFont("궁서", 20))
        self.ip_guide.setAlignment(QtCore.Qt.AlignCenter)
        self.ip_edit = QLineEdit()
        self.ip_btn = QPushButton('Change', self)
        self.ip_btn.clicked.connect(self.change_ip)

        #question guide line
        self.question_mark = QLabel("?", self)
        self.question_mark.resize(50, 50)
        self.question_mark.setFont(QtGui.QFont("궁서", 30))
        self.question_mark.setToolTip('<b>Eye Tracking Guide</b><br> </br> <br><b>STEP 1. </b>Enter Your name</br> <br><b>STEP 2. </b>Click Start button & Gaze red points</br>  <br><b>STEP 3. </b>When you want to stop the eye tracking, Press ESC and Click End button</br>')

        self.logo_label = QLabel(self)
        self.logo = QPixmap("EYE.png")
        self.logo = self.logo.scaledToWidth(500)
        self.logo_label.setPixmap(QPixmap(self.logo))
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        self.face_label = QtWidgets.QLabel(self)
        self.face_label.setFrameShape(QtWidgets.QFrame.Box)
        self.face_label.setFixedSize(800, 500)
        self.face_label.setObjectName("face_label")

        self.hello_user = QLabel(self)
        self.hello_user.setAlignment(QtCore.Qt.AlignCenter)

        self.name_guide = QLabel('Enter Your name')
        self.name_guide.setFont(QtGui.QFont("궁서", 20))
        self.name_guide.setAlignment(QtCore.Qt.AlignCenter)
        self.name_edit = QLineEdit()
        self.name_btn = QPushButton('OK', self)

        self.graph_label = QtWidgets.QLabel(self)
        self.graph_label.setFrameShape(QtWidgets.QFrame.Box)
        self.graph_label.setFixedSize(800, 500)
        self.graph_label.setAlignment(QtCore.Qt.AlignCenter)

        self.Stack = QStackedWidget(self)
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)
        self.name_btn.clicked.connect(self.change_display)

        #vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.logo_label)
        vbox.addWidget(self.Stack)

        self.setLayout(vbox)

        self.resize(900, 900)
        self.center()
        self.show()

    def change_display(self, text):
        self.Stack.setCurrentWidget(self.stack2)
        self.currentStack = 2
        self.name = self.name_edit.text()
        self.hello_user.setText("Hello "+self.name+"!")
        self.hello_user.setFont(QtGui.QFont("궁서", 20))
        self.logo = self.logo.scaledToWidth(200)
        self.logo_label.setPixmap(QPixmap(self.logo))


    def stack1UI(self):
        #name text
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.name_edit)
        hbox.addWidget(self.name_btn)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.name_guide)
        vbox.addLayout(hbox)
        vbox.addStretch(15)
        self.stack1.setLayout(vbox)

    def stack2UI(self):
        #face
        fhbox = QHBoxLayout()
        fhbox.addStretch(1)
        fhbox.addWidget(self.face_label)
        fhbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.start_btn)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.hello_user)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(fhbox)
        vbox.addStretch(1)
        self.stack2.setLayout(vbox)

    def stack3UI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.graph_label)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.stack3.setLayout(vbox)

    def stack4UI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.ip_edit)
        hbox.addWidget(self.ip_btn)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.ip_guide)
        vbox.addLayout(hbox)
        vbox.addStretch(15)
        self.stack4.setLayout(vbox)

    def set_ip(self, state):
        if state:
            self.setting.setText("Back")
            self.Stack.setCurrentWidget(self.stack4)
            self.ip_guide.setText('current IP Address : ' + database_func.host)
            if bool(self.ip_btn.isChecked()):
                self.ip_btn.clicked.connect(self.change_ip)
        else:
            self.setting.setText("Setting")
            if self.currentStack == 1:
                self.Stack.setCurrentWidget(self.stack1)
            elif self.currentStack == 2:
                self.Stack.setCurrentWidget(self.stack2)
            else:
                self.Stack.setCurrentWidget(self.stack3)

    def change_ip(self):
        self.ip = self.ip_edit.text()
        database_func.host = self.ip
        self.ip_guide.setText('current IP Address : ' + database_func.host)

    def start_end(self, state):
        if state:
            self.start_btn.setText("End")
            return 1
        else:
            self.start_btn.setText("Start")
            return 0

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.quit_sig = True
            event.accept()
        else:
            self.quit_sig = False
            event.ignore()

