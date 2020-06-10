import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import json
import zmq
from threading import Thread
import System.Data.CONSTANTS as portsFile
from System.CameraNode import CameraNode
import time
import random

vidpath = ''
cities = ['Cairo', 'Alexandria', 'Gizah', 'Shubra El-Kheima', 'Port Said', 'Suez', 'Luxor', 'Al-Mansura',
          'El-Mahalla El-Kubra', 'Tanta', 'Asyut', 'Ismailia', 'Fayyum', 'Zagazig', 'Aswan', 'Damietta',
          'Damanhur', 'Al-Minya', 'Beni Suef', 'Qena', 'Sohag', 'Hurghada', '6th of October City', 'Shibin El Kom',
          'Banha', 'Kafr el-Sheikh', 'Arish', 'Mallawi', '10th of Ramadan City', 'Bilbais', 'Marsa Matruh',
          'Idfu, Mit Ghamr', 'Al-Hamidiyya', 'Desouk', 'Qalyub', 'Abu Kabir', 'Kafr el-Dawwar', 'Girga', 'Akhmim', 'Matareya']


class WorkerThread(QObject):
    temp = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            time.sleep(1)
            self.temp.emit()
            # print('hit it')


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


class SearchForm(QWidget):
    def __init__(self, port=portsFile.MASTERPORT):
        super().__init__()

        self.worker = WorkerThread()
        self.workerThread = QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.temp.connect(self.temp)  # Connect your signals/slots
        self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
        self.workerThread.start()
        self.showLoading = False

        self.setWindowTitle('Argus')
        self.setGeometry(350, 90, 629, 597)
        self.setFixedSize(629, 597)

        self.processing_lable = self.make_lable('Processing....', 290, 305, 151, 41, True, 12)
        self.processing_lable.setVisible(False)
        self.gif = QMovie('UI/loading.gif')
        self.gif.setScaledSize(QSize().scaled(60, 60, Qt.KeepAspectRatio))
        self.processing_lable.setMovie(self.gif)
        self.gif.start()

        self.select_vid = Button("", self)
        self.select_vid.setText('Drag and Drop')
        self.select_vid.move(140, 20)
        self.select_vid.resize(351, 241)
        self.select_vid.clicked.connect(self.getfiles)
        font = QFont('SansSerif', 14)
        font.setBold(True)
        self.select_vid.setFont(font)


        self.play_vid = QPushButton(self)
        self.play_vid.setVisible(False)

        process = QPushButton(self)
        process.setText('Process')
        process.move(280, 270)
        process.resize(75, 23)
        process.clicked.connect(self.sendToBk)

        self.results = QListWidget(self)
        self.results.move(140, 350)
        self.results.resize(351, 241)
        self.results.setVisible(False)

        # Initialize connection
        context = zmq.Context()
        print("Connecting to server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:%s" % port)

        # Initialize results container
        self.results = []

    def sendToBk(self):
        global vidpath, cities
        self.processing_lable.setVisible(True)
        # self.temp()
        # self.showLoading = True
        import time
        # time.sleep(1)
        # path = json.dumps(vidpath)
        # self.socket.send_json(path)
        video_id = vidpath.split('.')[0]
        video_id = video_id.split('/')
        video_id = int(video_id[-1])
        print("hello")
        CameraNode(video_id, 'videos/' + str(video_id) + '.mp4',files=True, city= random.choice(cities), district_no= 'District ' + str(random.randint(1, 30))).start()
        self.playVideo()

        # thread = Thread(target=self.temp)
        # thread.start()
        # resultsJson = thread.join()
        # resultsJson = self.socket.recv_json()
        # self.decodeJson(resultsJson)
        # self.displayResults()
        # self.results.setVisible(True)

    def temp(self):
        try:
            resultsJson = self.socket.recv(flags=zmq.NOBLOCK)
            # print(resultsJson, '--------------')

            # self.decodeJson(resultsJson)
        except:
            return
        # self.processing_lable.setVisible(True)
        return

    def receiveJson(self):
        resultsJson = self.socket.recv_json()
        return resultsJson


    def decodeJson(self, compressed):
        self.results = json.dumps(compressed)

    def displayResults(self):
        pass

    def playVideo(self):
        global vidpath
        print(vidpath)
        cap = cv2.VideoCapture(vidpath)

        if (cap.isOpened() == False):
            print("Error opening video  file")

        while (cap.isOpened()):
            # time.sleep(1)
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(31) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()


    def getfiles(self):
        global vidpath
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', 'C:\'', '*.mp4 *.mkv *.avi')
        # self.label.setPixmap(QPixmap(fileName))
        # self.ui.lineEdit.setText(fileName)
        self.loadVideo(path=fileName)
        vidpath = fileName
        print(vidpath,'vid')
        print(fileName)

    def loadVideo(self, path='h.mp4'):
        cap = cv2.VideoCapture(path)
        ret, frame = cap.read()

        img = cv2.resize(frame, (351, 241), interpolation=cv2.INTER_AREA)
        # height, width, channel = img.shape
        # bytesPerLine = 3 * width
        # qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_BGR888)
        # pixmap = QPixmap(qImg)
        #
        # img_lable = self.make_lable('', 140, 20, 351, 241)
        # img_lable.setPixmap(pixmap)
        # img_lable.setVisible(True)

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
        # img = new
        cv2.imwrite('UI/tempToLoad.png', border)
        print('reached')
        # self.select_vid.setVisible(False)
        # play_vid = QPushButton(self)
        self.play_vid.setText('')
        self.play_vid.move(140, 20)
        self.play_vid.resize(351, 241)
        self.play_vid.setStyleSheet("background-image : url(UI/tempToLoad.png);")
        self.play_vid.clicked.connect(self.playVideo)
        self.play_vid.setVisible(True)

        # height, width, channel = img.shape
        # bytesPerLine = 3 * width
        # qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_BGR888)
        # pixmap = QPixmap(qImg)
        #
        # img_lable = self.make_lable('', 140, 20, 351, 241)
        # img_lable.setPixmap(pixmap)
        # img_lable.setVisible(True)
        # img_lable.linkActivated.connect(self.playVideo)


    def listwidgetclicked(self, item):
        print(item.text())

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

    form = SearchForm()
    form.show()
    sys.exit(app.exec_())
