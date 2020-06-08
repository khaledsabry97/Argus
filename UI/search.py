import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QCalendarWidget
from PyQt5.QtCore import *
# from PyQt5.QtCore import
# from datetime import datetime
# import calendar
import cv2
class SearchForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Argus')
        self.setGeometry(330, 150, 731, 438)
        # self.setGeometry(300, 300, 1200, 1200)

        # layout = QGridLayout()

        self.make_lable('Date', 60, 0, 61, 41, True, 12)
        self.make_lable('From', 10, 40, 41, 21, True, 10)
        self.make_lable('To', 10, 70, 41, 21, True, 10)

        self.make_lable('Time', 250, 0, 61, 41, True, 12)
        self.make_lable('From', 190, 40, 41, 21, True, 10)
        self.make_lable('To', 190, 70, 41, 21, True, 10)

        self.make_lable('City', 400, 0, 61, 41, True, 12)
        self.make_lable('Location', 520, 0, 81, 41, True, 12)

        startDate = QDateEdit(self)
        startDate.move(50, 40)
        startDate.resize(110, 22)
        endDate = QDateEdit(self)
        endDate.move(50, 70)
        endDate.resize(110, 22)

        startTime = QTimeEdit(self)
        startTime.move(230, 40)
        startTime.resize(110, 22)
        endTime = QTimeEdit(self)
        endTime.move(230, 70)
        endTime.resize(110, 22)

        city = QLineEdit(self)
        city.move(370, 40)
        city.resize(110, 22)

        loc = QLineEdit(self)
        loc.move(500, 40)
        loc.resize(110, 22)

        search = QPushButton(self)
        search.setText('Search')
        search.move(640, 40)
        search.resize(71, 51)

        self.results = QListWidget(self)
        self.results.move(20, 120)
        self.results.resize(691, 301)

        # results.addItem(QListWidgetItem('item1'))
        # results.addItem(QListWidgetItem('item2'))
        # results.itemDoubleClicked.connect(self.listwidgetclicked)

        itemN = QListWidgetItem()
        # Create widget
        widget = QWidget()
        widgetText = QLabel()
        img = cv2.imread('Untitled.png')
        img = cv2.resize(img, (91, 41), interpolation=cv2.INTER_AREA)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_BGR888)
        pixmap = QPixmap(qImg)
        widgetText.setPixmap(pixmap)
        widgetText.resize(15, 15)
        widgetButton = QPushButton("Push Me")
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(widgetButton)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(widgetLayout)
        itemN.setSizeHint(widget.sizeHint())

        self.results.addItem(itemN)
        self.results.setItemWidget(itemN, widget)

    def listwidgetclicked(self, item):
        print(item.text())

    def make_lable(self, name, x, y, width, height, bold=False, font=12):
        label = QLabel(self)
        label.setText(name)
        label.move(x, y)
        label.resize(width, height)
        font = QFont('SansSerif', font)
        if bold:
            font.setBold(True)
        label.setFont(font)
        return label

    # def display_results(self, results_list):



    def set_date(self, qDate):
        print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = SearchForm()
    form.show()
    sys.exit(app.exec_())