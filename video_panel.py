# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video_lbl.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_lbl = QtWidgets.QLabel(self.centralwidget)
        self.video_lbl.setGeometry(QtCore.QRect(130, 20, 571, 361))
        self.video_lbl.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"background-color: rgb(97, 97, 97);")
        self.video_lbl.setText("")
        self.video_lbl.setObjectName("video_lbl")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 390, 571, 41))
        self.pushButton.setObjectName("pushButton")
        self.stop_cam = QtWidgets.QPushButton(self.centralwidget)
        self.stop_cam.setGeometry(QtCore.QRect(130, 440, 571, 41))
        self.stop_cam.setObjectName("stop_cam")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Get video from camera"))
        self.stop_cam.setText(_translate("MainWindow", "Stop camera"))
