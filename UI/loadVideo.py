import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import zmq
from System.Data.CONSTANTS import *
from System.CameraNode import CameraNode
import random

vidpath = ''
cities = ['Cairo', 'Alexandria', 'Gizah', 'Shubra El-Kheima', 'Port Said', 'Suez', 'Luxor', 'Al-Mansura',
         'Tanta', 'Asyut', 'Ismailia', 'Fayyum', 'Zagazig', 'Aswan', 'Damietta',
          'Damanhur', 'Al-Minya', 'Beni Suef', 'Qena', 'Sohag', 'Hurghada', 'Shibin El Kom',
          'Banha', 'Arish', 'Mallawi', 'Bilbais', 'Marsa Matruh',
          'Idfu, Mit Ghamr', 'Al-Hamidiyya', 'Desouk', 'Qalyub', 'Abu Kabir', 'Girga', 'Akhmim', 'Matareya']


class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        m = e.mimeData()
        if m.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        global vidpath
        m = e.mimeData()
        if m.hasUrls():
            # self.parent().label.setPixmap(QPixmap(m.urls()[0].toLocalFile()))
            self.parent().loadVideo(m.urls()[0].toLocalFile())
            vidpath = m.urls()[0].toLocalFile()
            print(m.urls()[0].toLocalFile())


class Client(QWidget):
    def __init__(self, port=MASTERPORT, ip=MASTERIP):
        super().__init__()

        self.setWindowTitle('Argus - Camera Node')
        self.setWindowIcon(QIcon('UI/icon.png'))
        self.setGeometry(350, 90, 629, 597)
        self.setFixedSize(615, 419)

        self.processing_lable = self.make_lable('Processing....', 0, 0, 40, 40, True, 12)
        self.processing_lable.setVisible(False)
        self.gif = QMovie('UI/loading.gif')
        self.gif.setScaledSize(QSize().scaled(40, 40, Qt.KeepAspectRatio))
        self.processing_lable.setMovie(self.gif)
        self.gif.start()

        self.select_vid = Button("", self)
        self.select_vid.setText('Select video')
        self.select_vid.move(170, 20)
        self.select_vid.resize(91,71)
        self.select_vid.clicked.connect(self.getfiles)
        font = QFont('SansSerif', 9)
        font.setBold(True)
        self.select_vid.setFont(font)


        self.play_vid = QPushButton(self)
        self.play_vid.setStyleSheet("background-color: #000000;")
        self.play_vid.setText('')
        self.play_vid.move(30, 105)
        self.play_vid.resize(559, 300)
        self.play_vid.clicked.connect(self.playVideo)

        process = QPushButton(self)
        process.setText('Process')
        process.move(350, 20)
        process.resize(91,71)
        process.clicked.connect(self.sendToBk)
        process.setFont(font)

        # Initialize connection
        context = zmq.Context()
        print("Connecting to server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://"+ip+":"+str(port))

    def sendToBk(self):
        global vidpath, cities

        if vidpath=='':
            return

        self.processing_lable.setVisible(True)

        video_id = vidpath.split('.')[0]
        video_id = video_id.split('/')
        video_id = int(video_id[-1])
        print("hello")
        CameraNode(video_id, 'videos/' + str(video_id) + '.mp4',files=True, city= random.choice(cities), district_no= 'District ' + str(random.randint(1, 30))).start()
        self.playVideo()


    def playVideo(self):
        global vidpath
        print(vidpath)
        if vidpath=='':
            return

        cap = cv2.VideoCapture(vidpath)

        if (cap.isOpened() == False):
            print("Error opening video  file")

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame', frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()


    def getfiles(self):
        global vidpath

        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', 'C:\'', '*.mp4 *.mkv *.avi')

        if fileName=='':
            return

        self.loadVideo(path=fileName)
        vidpath = fileName
        print(vidpath,'vid')
        print(fileName)

    def loadVideo(self, path='h.mp4'):
        cap = cv2.VideoCapture(path)
        ret, frame = cap.read()

        img = cv2.resize(frame, (351, 241), interpolation=cv2.INTER_AREA)

        button = cv2.imread('UI/Play-Button-PNG-Picture.png')
        button = cv2.resize(button, (111, 111), interpolation=cv2.INTER_AREA)
        print(button.shape)
        print(img.shape)

        height_needed = 241 - button.shape[0]
        width_needed = 351 - button.shape[1]

        top = int(np.floor(height_needed / 2))
        bottom = int(np.ceil(height_needed / 2))
        left = int(np.floor(width_needed / 2))
        right = int(np.ceil(width_needed / 2))

        border = cv2.copyMakeBorder(button, top=top, bottom=bottom, left=left, right=right, borderType=cv2.BORDER_CONSTANT, value=0)
        border = np.where(border < 150, img, border)


        border = cv2.resize(border, (559, 300), interpolation=cv2.INTER_AREA)
        cv2.imwrite('UI/tempToLoad.png', border)
        # self.select_vid.setVisible(False)
        # play_vid = QPushButton(self)
        # self.play_vid.setText('')
        # self.play_vid.move(140, 20)
        # self.play_vid.resize(351, 241)
        self.play_vid.setStyleSheet("background-image : url(UI/tempToLoad.png);")
        # self.play_vid.clicked.connect(self.playVideo)
        # self.play_vid.setVisible(True)

    def make_lable(self, text, x, y, width, height, bold=False, font=12):
        label = QLabel(self)
        label.setText(text)
        label.move(x, y)
        label.resize(width, height)
        font = QFont('SansSerif', font)
        if bold:
            font.setBold(True)
        label.setFont(font)
        return label



if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = Client()
    form.show()
    sys.exit(app.exec_())
