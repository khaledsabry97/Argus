import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import time
import zmq
from numpy.core.multiarray import ndarray

from System.Data.CONSTANTS import *
from System.Controller.JsonEncoder import JsonEncoder

class WorkerThread(QObject):
    receive = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://"+GUIIP+":"+str(GUIPORT))

    @pyqtSlot()
    def run(self):
        while True:
            message = self.socket.recv_pyobj()  # receive a message json
            self.socket.send_pyobj("")
            self.receive.emit(message)


class SearchForm(QWidget):
    def __init__(self, port=GUIPORT, ip=GUIIP):
        super().__init__()

        self.encoder = JsonEncoder()

        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #D3D3D3;")
        self.setWindowTitle('Argus')
        # self.setStyleSheet(open('style.css').read())

        # self.setGeometry(330, 150, 731, 438)
        self.setGeometry(350, 50, 800, 850)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        oImage = QImage("Untitled.png")
        sImage = oImage.scaled(QSize(300, 200))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.worker = WorkerThread()
        self.workerThread = QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.receive.connect(self.decode)           # Connect your signals/slots
        self.worker.moveToThread(self.workerThread)         # Move the Worker object to the Thread object
        self.workerThread.start()

        self.make_lable('Date', 60, 0, 61, 41, True, 12)
        self.make_lable('From', 10, 40, 41, 21, True, 10)
        self.make_lable('To', 10, 70, 41, 21, True, 10)

        self.make_lable('Time', 250, 0, 61, 41, True, 12)
        self.make_lable('From', 190, 40, 41, 21, True, 10)
        self.make_lable('To', 190, 70, 41, 21, True, 10)

        self.make_lable('City', 400, 0, 61, 41, True, 12)
        self.make_lable('Location', 520, 0, 81, 41, True, 12)

        self.startDate = QDateEdit(self)
        self.startDate.move(50, 40)
        self.startDate.resize(110, 22)
        self.startDate.setDate(QDate.fromString('01/01/2015', "dd/MM/yyyy"))
        self.endDate = QDateEdit(self)
        self.endDate.move(50, 70)
        self.endDate.resize(110, 22)
        self.endDate.setDate(QDate.fromString('01/01/2015', "dd/MM/yyyy"))

        self.startTime = QTimeEdit(self)
        self.startTime.setDisplayFormat('hh:mm')
        self.startTime.move(230, 40)
        self.startTime.resize(110, 22)
        self.endTime = QTimeEdit(self)
        self.endTime.setDisplayFormat('hh:mm')
        self.endTime.move(230, 70)
        self.endTime.resize(110, 22)

        self.city = QLineEdit(self)
        self.city.move(370, 40)
        self.city.resize(110, 22)

        self.loc = QLineEdit(self)
        self.loc.move(500, 40)
        self.loc.resize(110, 22)


        search = QPushButton(self)
        search.setText('Search')
        search.move(270, 105)
        search.resize(71, 51)
        search.clicked.connect(self.searchClicked)

        reset = QPushButton(self)
        reset.setText('Recent')
        reset.move(370, 105)
        reset.resize(71, 51)
        reset.clicked.connect(self.recentlyClicked)

        self.results = QListWidget(self)
        self.results.move(20, 175)
        self.results.resize(760, 650)
        self.results.itemDoubleClicked.connect(self.listwidgetClicked)
        self.results.setStyleSheet("background-color: #C0C0C0;")

        widgetText = QLabel(self)
        widgetText.move(630, 15)
        img = QImage("logo.png")
        img.convertToFormat(QImage.Format_ARGB32)
        pixmap = QPixmap(img)
        pixmap = pixmap.scaled(134, 94, Qt.KeepAspectRatio)
        widgetText.setPixmap(pixmap)

        # self.appendToList(list=True)
        # self.appendToList(list=False)
        print("hello")
        self.recentlyClicked()

    def listwidgetClicked(self, item):
        item = self.results.itemWidget(item)
        info = item.children()[-1]
        startFrameID, cameraID = info.text().split(',')
        print(startFrameID, cameraID)
        self.encoder.requestVideo(camera_id=int(cameraID), starting_frame_id=int(startFrameID))
        return


    def searchClicked(self):
        city = None
        district = None

        if self.city.text() != '':
            city = self.city.text()
        if self.loc.text() != '':
            district = self.loc.text()

        self.encoder.requestData(self.startDate.text(), self.endDate.text(), self.startTime.text(), self.endTime.text(),
                                 city, district)

    def recentlyClicked(self):
        self.encoder.getRecentCrashes()


    def appendToList(self, ID=3, Image=None, Date='a', Time='d', City='f', Location='g', startFrame=1, list=True):
        itemN = QListWidgetItem()
        widget = QWidget()

        widgetText = QLabel()
        if not isinstance(Image,ndarray) :
            img = cv2.imread('notfound.png')
        else:
            img = Image
        img = cv2.resize(img, (120, 100), interpolation=cv2.INTER_AREA)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_BGR888)
        pixmap = QPixmap(qImg)
        widgetText.setPixmap(pixmap)
        widgetText.resize(20, 20)

        startFrameID = QLabel()
        startFrameID.setText(str(startFrame)+','+str(ID))
        startFrameID.hide()
        print(startFrameID.text())

        info = QLabel()
        font = QFont('SansSerif', 10)
        font.setBold(True)
        info.setFont(font)
        info.setText('   Camera Id: ' + str(ID) + '  Date: ' + str(Date) + '    City: ' + str(City)
                     + '   Location: ' + str(Location))
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(info)
        widgetLayout.addWidget(startFrameID)
        widgetLayout.addStretch()
        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(widgetLayout)
        widget.setStyleSheet("background-color: none;")
        # widget.paintEvent()
        itemN.setSizeHint(widget.sizeHint())
        if list:
            self.results.addItem(itemN)
            self.results.setItemWidget(itemN, widget)

        else:
            itemN.setBackground(QColor('#7fc97f'))
            self.results.insertItem(0, itemN)
            self.results.setItemWidget(itemN, widget)



    def make_lable(self, text, x, y, width, height, bold=False, font=12):
        label = QLabel(self)
        label.setText(text)
        label.move(x, y)
        label.resize(width, height)
        font = QFont('SansSerif', font)
        if bold:
            font.setBold(True)
        label.setFont(font)
        # label.setStyleSheet(open('style.css').read())

        return label

    def playVideo(self, video):
        for i in range(len(video)):
            cv2.imshow('Frame', video[i])
            if cv2.waitKey(31) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()





    def decode(self, msg):
        func = msg[FUNCTION]

        if func == REP_QUERY:
            self.results.clear()
            list = msg[LIST_OF_CRASHES]
            for item in list:
                self.appendToList(ID=item[CAMERA_ID], Image=item[CRASH_PIC], Date=item[CRASH_TIME], Time=item[CRASH_TIME],
                                  City=item[CITY], Location=item[DISTRICT], startFrame=item[STARTING_FRAME_ID], list=True)
            return

        if func == NOTIFICATION:
            self.appendToList(ID=msg[CAMERA_ID], Image=msg[CRASH_PIC], Date=msg[CRASH_TIME], Time=msg[CRASH_TIME],
                              City=msg[CITY], Location=msg[DISTRICT], startFrame=msg[STARTING_FRAME_ID], list=False)
            return

        if func == REP_VIDEO:
            self.playVideo(msg[FRAMES])
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = SearchForm()
    form.show()
    sys.exit(app.exec_())