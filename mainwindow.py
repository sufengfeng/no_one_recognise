#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_py.ui_main_window import Main_Form

Marviw_IP = "192.168.3.164"
#Marviw_IP = "127.0.0.1"
Marviw_Port = 502

Barracks_IP = "192.168.1.201"
Theaters_IP = "192.168.1.201"
Headquarters_IP = "192.168.1.201"

Slave_PORT = 502
Master_PORT = 502

g_KeyData = [1, 0, 32, 0, 4, 15, 0, 2, 0, 2, 0, 2, 255, 63, 255, 63, 130, 240, 128, 240, 129, 72, 195, 39, 197, 57, 8,
             2, 0, 0, 0, 0, 0, 0, 0, 0]

g_role = 1


CameraIP = "192.168.3.79"
CameraPort = 80
CameraUserName = "admin"
CameraPassword = "123456"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("PyQt MianWindow")
    app.setWindowIcon(QIcon("./images/icon.png"))

    MainWindow = Main_Form()
    MainWindow.show()
    sys.exit(app.exec_())


