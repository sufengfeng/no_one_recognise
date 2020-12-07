#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
from socket import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from json_message import MessageType, MessageType2dict
from ui.setup import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QMainWindow

PORT = 21567


class Setup_Form(QtWidgets.QDialog, Ui_Dialog):
    signal_SendParam = pyqtSignal(object, object, object, object, object, object)

    def __init__(self):
        super(Setup_Form, self).__init__()
        self.setupUi(self)

        self.pushButton_ok.clicked.connect(self.click_OK)
        self.pushButton_cancel.clicked.connect(self.close)

    def click_OK(self):
        stepx=int(self.lineEdit_stepx.text())
        speedx=int(self.lineEdit_speedx.text())
        stepy = int(self.lineEdit_stepy.text())
        speedy = int(self.lineEdit_speedy.text())
        self.signal_SendParam.emit(stepx, speedx, stepy, speedy, "tex5t", "text6")
        self.close()

    def setParam(self, stepx, speedx,stepy, speedy):

        self.lineEdit_stepx.setText(str(stepx))
        self.lineEdit_speedx.setText(str(speedx))
        self.lineEdit_stepy.setText(str(stepy))
        self.lineEdit_speedy.setText(str(speedy))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_motor = Setup_Form()

    ui_motor.show()
    sys.exit(app.exec_())
