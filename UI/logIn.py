import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox

class kak(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Argus')
        self.resize(500, 120)


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Argus')
        self.resize(500, 120)

        layout = QGridLayout()

        labelName = QLabel('<font size = "4"> Username </font>')
        labelPassword = QLabel('<font size = "4"> Password </font>')

        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Enter the username')
        layout.addWidget(labelName, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_password.setPlaceholderText('Enter the password')
        layout.addWidget(labelPassword, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)


        button_login = QPushButton('Log in')
        button_login.clicked.connect(self.check_password)
        
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)


    def check_password(self):
        msg = QMessageBox()

        if self.lineEdit_username.text() == 'Username' and self.lineEdit_password.text() == '111':
            msg.setText('Success')
            msg.exec_()
            app.quit()
        else:
            msg.setText('Incorrect Password')
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()
    sys.exit(app.exec_())