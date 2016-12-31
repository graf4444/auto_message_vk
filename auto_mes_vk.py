#coding: utf8
import sys
import vk
import webbrowser
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QDateTimeEdit
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui
from random import randint

app = QApplication(sys.argv)
app.setApplicationName('auto_message_vk')
from_class, base_class = loadUiType('auto_mes_vk_form.ui')


class MainWindow(QDialog, from_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.ui = from_class()
        self.ui.setupUi(self)

        self.ui.dateTimeEdit.setEnabled(False)

        self.ui.pushButton.clicked.connect(self.test)
        self.ui.pushButton_2.clicked.connect(self.get_token)
        self.ui.pushButton_3.clicked.connect(self.set_dateTime)
        self.ui.checkBox.stateChanged.connect(self.state_changed)

    def set_dateTime(self):
        self.ui.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

    def state_changed(self):
        if self.ui.checkBox.isChecked():
            self.ui.dateTimeEdit.setEnabled(True)
            # self.ui.label.setText(time.ctime(time.time()))
            # self.now = QtCore.QDateTime.currentDateTime()
            # print(self.now.secsTo(self.ui.dateTimeEdit.dateTime()))
        else:
            self.ui.dateTimeEdit.setEnabled(False)

    def get_token(self):
        webbrowser.open_new_tab(
            'https://oauth.vk.com/authorize?client_id=5210750&scope=friends,messages&response_type=token')

    def test(self):
        self.token = self.ui.lineEdit_token.text()

        self.session = vk.Session(access_token=self.token)
        self.api = vk.API(self.session)
        self.ui.label.setText('')


        self.ids = self.ui.textEdit.toPlainText().split('\n')
        for i in range(len(self.ids)):
            if self.ids[i].isdigit():
                self.ids[i] = int(self.ids[i])
            else:
                self.ui.label.setText(u'Ошибка! Введен неправильный id: "' + str(self.ids[i]) + u'" в ' + str(i+1) + u' строке!\nВводить только цифры id!')
                return;
        self.text = self.ui.textEdit_2.toPlainText()

        if self.ui.checkBox.isChecked():
            now = QtCore.QDateTime.currentDateTime()
            self.balance = now.secsTo(self.ui.dateTimeEdit.dateTime())
            time.sleep(self.balance)

        for id in self.ids:
            self.api.messages.send(user_id=id, message=self.text)
            time.sleep(randint(int(self.ui.spinBox.value()), int(self.ui.spinBox_2.value())))


#---------------------------------------------------------#
form = MainWindow()
form.setWindowTitle(u'Поздравлятор ver. 0.1')
form.show()
sys.exit(app.exec_())