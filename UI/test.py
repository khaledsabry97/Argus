# import sys
# from PyQt5 import QtCore, QtWidgets
#
#
# class MainWindow(QtWidgets.QWidget):
#
#     switch_window = QtCore.pyqtSignal(str)
#
#     def __init__(self):
#         QtWidgets.QWidget.__init__(self)
#         self.setWindowTitle('Main Window')
#
#         layout = QtWidgets.QGridLayout()
#
#         self.line_edit = QtWidgets.QLineEdit()
#         layout.addWidget(self.line_edit)
#
#         self.button = QtWidgets.QPushButton('Switch Window')
#         self.button.clicked.connect(self.switch)
#         layout.addWidget(self.button)
#
#         self.setLayout(layout)
#
#     def switch(self):
#         self.switch_window.emit(self.line_edit.text())
#
#
# class WindowTwo(QtWidgets.QWidget):
#
#     def __init__(self, text):
#         QtWidgets.QWidget.__init__(self)
#         self.setWindowTitle('Window Two')
#
#         layout = QtWidgets.QGridLayout()
#
#         self.label = QtWidgets.QLabel(text)
#         layout.addWidget(self.label)
#
#         self.button = QtWidgets.QPushButton('Close')
#         self.button.clicked.connect(self.close)
#
#         layout.addWidget(self.button)
#
#         self.setLayout(layout)
#
#
# class Login(QtWidgets.QWidget):
#
#     switch_window = QtCore.pyqtSignal()
#
#     def __init__(self):
#         QtWidgets.QWidget.__init__(self)
#         self.setWindowTitle('Login')
#
#         layout = QtWidgets.QGridLayout()
#
#         self.button = QtWidgets.QPushButton('Login')
#         self.button.clicked.connect(self.login)
#
#         layout.addWidget(self.button)
#
#         self.setLayout(layout)
#
#     def login(self):
#         self.switch_window.emit()
#
#
# class Controller:
#
#     def __init__(self):
#         pass
#
#     def show_login(self):
#         self.login = Login()
#         self.login.switch_window.connect(self.show_main)
#         self.login.show()
#
#     def show_main(self):
#         self.window = MainWindow()
#         self.window.switch_window.connect(self.show_window_two)
#         self.login.close()
#         self.window.show()
#
#     def show_window_two(self, text):
#         self.window_two = WindowTwo(text)
#         self.window.close()
#         self.window_two.show()
#
#
# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     controller = Controller()
#     controller.show_login()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()

import cv2

vidcap = cv2.VideoCapture('1.mp4')
print(vidcap)
