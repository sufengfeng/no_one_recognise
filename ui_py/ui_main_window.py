#!/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser

import sys
import threading
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from configure import CameraIP
from modbusMaster import modbusSetSpeed, modbusSetABS, modbusReadRist, SensorRigist01, SensorRigist02, SensorRigist03, \
    SensorRigist04, SensorRigist05, modbusWriteRist, REGIST_ABSX02, REGIST_ABSY02, REGIST_ABSY01, REGIST_ABSX01, \
    DORigest02_01, DORigest01_01, DORigest02_02, DORigest01_02, DORigest02_03, DORigest01_03, DORigest02_04, \
    DORigest01_04, Sensorauto

from setzoom import zoomtele, zoomstop, zoomwide, zoomcam
from ui.main_window import Ui_MainWindow
from ui_py.ui_gis import Gis_Form
from ui_py.ui_setup import Setup_Form
import ui.py_img

g_nSpeedx = 30
g_nStepx = 1
g_nSpeedy = 30
g_nStepy = 1
TMPIMGFILE = ":/tmp.jpg"

from mouse_qt import g_bScondEnable


class Main_Form(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Form, self).__init__()
        self.setupUi(self)

        self.shut01Value = False
        self.shut02Value = False
        self.shut03Value = False
        self.shut04Value = False
        self.isScan = False

        self.m_bIsSensor = False  # 使能传感器
        self.m_bIsOpenVideo = False  # 使能视频


        self.label_img.setStyleSheet("border: 2px solid red")
        # self.pushButton_des.clicked.connect(self.On_DesClick)

        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time)
        # self.timer.start(50)

        # self.timer_face = QTimer()  # 初始化定时器
        # self.timer_face.timeout.connect(self.face_beautify)
        # self.timer_face.start(1000)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_up.setIcon(icon)
        self.pushButton_up.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_up.setAutoRepeatDelay(200)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_down.setIcon(icon)
        self.pushButton_down.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_down.setAutoRepeatDelay(200)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/lift.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_lift.setIcon(icon)
        self.pushButton_lift.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_lift.setAutoRepeatDelay(200)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_right.setIcon(icon)
        self.pushButton_right.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_right.setAutoRepeatDelay(200)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/shut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_shut01.setIcon(icon)
        self.pushButton_shut01.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_shut01.setAutoRepeatDelay(200)

        self.pushButton_shut02.setIcon(icon)
        self.pushButton_shut02.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_shut02.setAutoRepeatDelay(200)

        self.pushButton_shut03.setIcon(icon)
        self.pushButton_shut03.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_shut03.setAutoRepeatDelay(200)

        self.pushButton_shut04.setIcon(icon)
        self.pushButton_shut04.setIconSize(QtCore.QSize(50, 80))
        self.pushButton_shut04.setAutoRepeatDelay(200)

        # self.setStyleSheet("#MainWindow{border-image:url(:/images/background.png);}")

        self.action_setup.triggered.connect(self.setParam)
        self.actionGIS_2.triggered.connect(self.openGis)

        self.pushButton_up.clicked.connect(self._up)
        self.pushButton_down.clicked.connect(self._down)
        self.pushButton_lift.clicked.connect(self._lift)
        self.pushButton_right.clicked.connect(self._right)

        self.pushButton_shut01.clicked.connect(self._shut01)
        self.pushButton_shut02.clicked.connect(self._shut02)
        self.pushButton_shut03.clicked.connect(self._shut03)
        self.pushButton_shut04.clicked.connect(self._shut04)
        self.pushButton_scan.clicked.connect(self._scan)

        # 创建视频更新线程
        t1 = threading.Thread(target=self.updateImg_thread, args=(100,))
        t1.start()
        # 创建遥信数据更新线程
        t1 = threading.Thread(target=self.updateSensorData, args=(100,))
        t1.start()

        # 创建遥信数据更新线程
        t1 = threading.Thread(target=self.scanSend, args=(100,))
        t1.start()

        self.checkBox_video.stateChanged.connect(self.changecb1)
        self.checkBox_sensor.stateChanged.connect(self.changecb2)
        # self.checkBox_hand.stateChanged.connect(self.changecb3)
        self.checkBox_plat.stateChanged.connect(self.changecb4)
        self.checkBox_auto.stateChanged.connect(self.changecb5)
        self.cam = zoomcam(CameraIP)
        self.pushButton_zoom01.clicked.connect(self.Zoom01)
        self.pushButton_zoom02.clicked.connect(self.Zoom02)

    def changecb1(self):
        if self.checkBox_video.checkState() == Qt.Checked:
            self.m_bIsOpenVideo = True
        elif self.checkBox_video.checkState() == Qt.Unchecked:
            self.m_bIsOpenVideo = False
            pix = QPixmap(':/images/nosignal.jpg')
            self.label_img.setGeometry(0, 0, pix.width(), pix.height())
            self.label_img.setPixmap(pix)

    def changecb2(self):
        if self.checkBox_sensor.checkState() == Qt.Checked:
            self.m_bIsSensor = True
        elif self.checkBox_sensor.checkState() == Qt.Unchecked:
            self.m_bIsSensor = False

    # def changecb3(self):
    #     if self.checkBox_hand.checkState() == Qt.Checked:
    #         self.m_bIsHand = True
    #     elif self.checkBox_hand.checkState() == Qt.Unchecked:
    #         self.m_bIsHand = False

    def changecb4(self):
        global g_bScondEnable
        if self.checkBox_plat.checkState() == Qt.Checked:
            g_bScondEnable = True
        elif self.checkBox_plat.checkState() == Qt.Unchecked:
            g_bScondEnable = False

    def changecb5(self):
        if self.checkBox_auto.checkState() == Qt.Checked:
            print(modbusWriteRist(Sensorauto, 1))
        elif self.checkBox_auto.checkState() == Qt.Unchecked:
            print(modbusWriteRist(Sensorauto, 0))

    def _up(self):
        global g_nSpeedx
        global g_nStepx
        global g_nSpeedy
        global g_nStepy

        modbusSetABS(self.REGIST_ABSY(), -g_nStepy)

    def _down(self):
        global g_nSpeedx
        global g_nStepx
        global g_nSpeedy
        global g_nStepy
        modbusSetABS(self.REGIST_ABSY(), g_nStepy)

    def _lift(self):
        global g_nSpeedx
        global g_nStepx
        global g_nSpeedy
        global g_nStepy
        modbusSetABS(self.REGIST_ABSX(), -g_nStepx)

    def _right(self):
        global g_nSpeedx
        global g_nStepx
        global g_nSpeedy
        global g_nStepy
        modbusSetABS(self.REGIST_ABSX(), g_nStepx)

    def setParam(self):
        global g_nSpeedx
        global g_nStepx
        global g_nSpeedy
        global g_nStepy

        ui_motor = Setup_Form()
        ui_motor.setParam(g_nStepx, g_nSpeedx, g_nStepy, g_nSpeedy)
        ui_motor.signal_SendParam.connect(self.receiveParam)
        ui_motor.exec()

    def openGis(self):

        # ui_motor.signal_SendParam.connect(self.receiveParam)

        self.form2_ = Gis_Form()
        #form2_.setWindowModality(True)
        self.form2_.show()

    def receiveParam(self, stepx, speedx, stepy, speedy, param05, param06):
        global g_nSpeedx
        global g_nStepx
        global g_nSpeedy
        global g_nStepy
        g_nStepx = stepx
        g_nSpeedx = speedx
        g_nStepy = stepy
        g_nSpeedy = speedy

        modbusSetSpeed(g_nSpeedx, g_nStepx, g_nSpeedy, g_nStepy)

    def _shut01(self):
        self.shut01Value = not self.shut01Value
        modbusWriteRist(self.DORigest01(), self.shut01Value)

    def _shut02(self):
        self.shut02Value = not self.shut02Value
        modbusWriteRist(self.DORigest02(), self.shut02Value)

    def _shut03(self):
        self.shut03Value = not self.shut03Value
        modbusWriteRist(self.DORigest03(), self.shut03Value)

    def _shut04(self):
        self.shut04Value = not self.shut04Value
        modbusWriteRist(self.DORigest04(), self.shut04Value)

    def _scan(self):
        self.isScan = not self.isScan

    def time(self):
        pass

    def updateImg_thread(self, param):
        import cv2, numpy

        # show nosignal.jpg to init
        pix = QPixmap(':/images/nosignal.jpg')
        self.label_img.setGeometry(0, 0, pix.width(), pix.height())
        self.label_img.setPixmap(pix)

        cam_addr = "rtsp://admin:123456@"+CameraIP+"/mpeg4cif" # camera address
        preIsOpen = False # pre state is open or not
        camOpened = False # cam is open or not
        oldSize = {"width":0, "height":0}
        while True:
            if self.m_bIsOpenVideo and not preIsOpen:
                # switch to Open from Close
                cap = cv2.VideoCapture(cam_addr)
                if cap.isOpened:
                    camOpened = True
                preIsOpen = True
            if camOpened:
                ret, frame = cap.read()
                if ret:
                    frame = cv2.resize(frame, (900, 529))
                    # cv2.imshow("img", frame)
                    # cv2.waitKey(1)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, depth = frame_rgb.shape
                    pix = QPixmap.fromImage(QImage(frame_rgb.data, width, height, width * depth, QImage.Format_RGB888))
                    if width != oldSize["width"] or height != oldSize["height"]:
                        self.label_img.setGeometry(0, 0, width, height)
                        oldSize["width"], oldSize["height"] = width, height
                    self.label_img.setPixmap(pix)
                else:
                    print("read frame failed.")
            if not self.m_bIsOpenVideo:
                if preIsOpen:
                    pix = QPixmap(':/images/nosignal.jpg')
                    self.label_img.setGeometry(0, 0, pix.width(), pix.height())
                    self.label_img.setPixmap(pix)
                    if camOpened:
                        cap.release() # close camera
                        camOpened = False
                    preIsOpen = False
                else:
                    sleep(0.05)

    def updateSensorData(self, param):
        while 1:
            if self.m_bIsSensor:
                value = modbusReadRist(SensorRigist01)
                self.label_sensor01.setText("传感器01：" + str(value))
                value = modbusReadRist(SensorRigist02)
                self.label_sensor02.setText("传感器02：" + str(value))
                value = modbusReadRist(SensorRigist03)
                self.label_sensor03.setText("传感器03：" + str(value))
                value = modbusReadRist(SensorRigist04)
                self.label_sensor04.setText("传感器04：" + str(value / 10))
                value = modbusReadRist(SensorRigist05)
                self.label_sensor05.setText("传感器05：" + str(value / 10))

            sleep(0.1)

    def scanSend(self, param):
        scan_step = 30
        while 1:
            if self.isScan:
                if scan_step == 30 or scan_step == 60:
                    scan_step = -60
                elif scan_step == -60:
                    scan_step = 60

                modbusSetABS(self.REGIST_ABSX(), scan_step)
            sleep(3)

    def REGIST_ABSY(self):
        global g_bScondEnable
        if g_bScondEnable:
            return REGIST_ABSY02
        else:
            return REGIST_ABSY01

    def REGIST_ABSX(self):
        global g_bScondEnable
        if g_bScondEnable:
            return REGIST_ABSX02
        else:
            return REGIST_ABSX01

    def DORigest01(self):
        global g_bScondEnable
        if g_bScondEnable:
            return DORigest02_01
        else:
            return DORigest01_01

    def DORigest02(self):
        global g_bScondEnable
        if g_bScondEnable:
            return DORigest02_02
        else:
            return DORigest01_02

    def DORigest03(self):
        global g_bScondEnable
        if g_bScondEnable:
            return DORigest02_03
        else:
            return DORigest01_03

    def DORigest04(self):
        global g_bScondEnable
        if g_bScondEnable:
            return DORigest02_04
        else:
            return DORigest01_04

    def Zoom01(self):
        self.cam.zoomwide(0.2)

    def Zoom02(self):
        self.cam.zoomtele(0.2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec_())
