from PyQt5 import QtWidgets
from video_panel import Ui_MainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from PyQt5.QtCore import  QTimer

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()



    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False

        self.wait()

class mywindow(QtWidgets.QMainWindow, QWidget):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # обработка нажатия кнопок на панели
        self.ui.pushButton.clicked.connect(self.camera_start)
        self.ui.stop_cam.clicked.connect(self.closeEvent)
        self.setWindowTitle("video_stream")
        self.cam_refresh = QTimer()  # таймера на камеру
        self.cam_refresh.timeout.connect(self.camera_start)
        self.disply_width = 640
        self.display_height = 480
    def camera_stop(self):
        self.thread.stop()
        self.video_lbl.setStyleSheet("background-color: rgb(0, 0, 0);\n")
    def camera_start(self):
        print('camera_start')
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()



    def closeEvent(self, event):
        print('stop')
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        print('update_image')
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        print('process')
        self.ui.video_lbl.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        print('convert_cv_qt')
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec_())