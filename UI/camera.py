import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=30):
        super().__init__()

        self.capture = cv2.VideoCapture(camera_index)
        self.dimensions = self.capture.read()[1].shape[1::-1]

        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)

        view = QGraphicsView(self)
        view.setScene(scene)

        text = QLabel('MegaWebcam 5.5', self)

        layout = QVBoxLayout(self)
        layout.addWidget(view)
        layout.addWidget(text)

        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def get_frame(self):
        _, frame = self.capture.read()
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)


app = QApplication([])
win = MainWindow()
win.show()
app.exec()