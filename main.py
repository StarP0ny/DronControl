from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer

from PyQt5.QtGui import QPixmap, QColor, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QObject
from interface import Ui_MainWindow
import sys
from djitellopy import tello
import cv2
from multiprocessing import  Pool

t = tello.Tello()
tello_map = []
#1-вперед, -1 назад; 2,-2 вверх, вниз; 3,-3 влево, вправо; 4,-4 по/против часовой
commands={1:'t.move_forward(20) ', -1:'t.move_back(20)', 2:'t.move_up(20)', -2:'t.move_down(20)', 3:'t.move_right(20)',-3:'t.move_left(20)', 4:'tello.rotate_clockwise(20)', -4:'t.rotate_counter_clockwise(20)'}


#try:
  #  t.connect()
  #  t.takeoff()
#except:
 #   print("pepeSad")

#Создаем новый класс, который называется mywindow путем наследования от класса QtWidgets.QMainWindow.

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.refresh = QTimer()

        self.refresh.timeout.connect(self.battery)
        self.ui.progressBar.setValue(100)
        self.cam_refresh = QTimer()  # таймера на камеру
        self.cam_refresh.timeout.connect(self.camera)
        self.bat_refresh = QTimer()  # таймера на батарею
        self.bat_refresh.timeout.connect(self.charge)

        palette = self.ui.lcdNumber.palette()
        # palette.setColor(palette.WindowText, QtGui.QColor(85, 85, 255))
        # background color
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        # "light" border
        palette.setColor(palette.Light, QtGui.QColor(0, 0, 0))

        self.ui.lcdNumber.setPalette(palette)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton.clicked.connect(self.btnClicked_Connect)
        self.ui.pushButton_12.clicked.connect(self.btnClicked_Land)
        self.ui.pushButton_10.clicked.connect(self.btnClicked_Start)
        self.ui.pushButton_11.clicked.connect(self.btnClicked_Stop)
        self.ui.pushButton_7.clicked.connect(self.btnClicked_Forward)
        self.ui.pushButton_18.clicked.connect(self.btnClicked_Back)
        self.ui.pushButton_6.clicked.connect(self.btnClicked_Right)
        self.ui.pushButton_8.clicked.connect(self.btnClicked_Left)
        self.ui.pushButton_9.clicked.connect(self.btnClicked_Up)
        self.ui.pushButton_5.clicked.connect(self.btnClicked_Down)
        self.ui.pushButton_2.clicked.connect(self.btnClicked_Rotate_clock)
        self.ui.pushButton_4.clicked.connect(self.btnClicked_Rotate_contr)
        self.ui.pushButton_14.clicked.connect(self.btnClicked_AutoReturn)
        self.setWindowTitle("Tello control panel")

    def charge(self):
        ch = t.get_height()
        h = t.query_wifi_signal_noise_ratio()

        self.ui.progressBar_2.setValue(ch)
        self.ui.progressBar.setValue(int(h))
        self.ui.lcdNumber.display(ch)

    def battery(self):
        t.rotate_clockwise(0)

    def camera(self):
        cv_img = t.get_frame_read().frame
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.label_7.setPixmap(qt_img)

    def btnClicked_Stop(self):
        t.streamoff()

    def btnClicked_Connect(self):
        self.ui.label.setText("Взлет")

        try:
            t.connect()
            t.takeoff()
        except:
            pass
        self.ui.label_3.setText("Воздух")
        self.refresh.start(4000)
        # Если не использовать, то часть текста исчезнет.
        self.ui.label.adjustSize()

    def btnClicked_Land(self):
        self.ui.label_3.setText("Посадка")
        t.land()
        self.refresh.stop()
        print(tello_map)

    def btnClicked_Forward(self):
        t.move_forward(20)
        tello_map.append(1)

    def btnClicked_Back(self):
        t.move_back(20)
        tello_map.append(-1)

    def btnClicked_Right(self):
        t.move_right(20)
        tello_map.append(3)

    def btnClicked_Left(self):
        t.move_left(20)
        tello_map.append(-3)

    def btnClicked_Up(self):
        t.move_up(20)
        tello_map.append(2)

    def btnClicked_Down(self):
        t.move_down(20)
        tello_map.append(-2)

    def btnClicked_Rotate_clock(self):
        t.rotate_clockwise(20)
        tello_map.append(4)

    def btnClicked_Rotate_contr(self):
        t.rotate_counter_clockwise(20)
        tello_map.append(-4)

    def btnClicked_Start(self):
        t.connect()
        #self.camera()
        t.streamon()
        self.cam_refresh.start(40)
        self.bat_refresh.start(6000)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(500, 281, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def btnClicked_AutoReturn(self):
        new_map = reversed(tello_map)
        new_map = [-x for x in new_map]
        print(tello_map)
        print(new_map)


#Добавляем строки для отображения окна:

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())