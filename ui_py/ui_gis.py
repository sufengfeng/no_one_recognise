#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import threading
from socket import *
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from PyQt5.QtGui import QPalette, QPixmap, QBrush
from modbusMaster import modbusReadRist, SensorRigist01, SensorRigist02, SensorRigist03, SensorRigist04, SensorRigist05
from mouse_qt import rocking_thread, server_target, qtsample_handler

from PyQt5.QtWidgets import QApplication

from ui.GIS import Ui_MainWindow_GIS

PORT = 21567
import pywinusb.hid as hid
import ui.py_img

class Gis_Form(QtWidgets.QMainWindow, Ui_MainWindow_GIS):
    # signal_SendParam = pyqtSignal(object, object, object, object, object, object)

    def __init__(self):
        super(Gis_Form, self).__init__()
        self.setupUi(self)

        self.resize(1900, 1000)
        self.setFixedSize(self.width(), self.height())
        self.isRuning = True

        self.enableSensor = False

        palette = QPalette()
        pix = QPixmap(":/images/gis.png")
        # self.resize(pix.width()*0.5,pix.height()*0.5)
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

        mark = 0.3
        ######################################################################
        pix = QPixmap(':/images/plan01.png')
        self.label_imgplanlong.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgplanlong.setPixmap(pix)
        self.label_imgplanlong.setScaledContents(True)  # 让图片自适应label大小

        self.label_imgplanlong_2.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgplanlong_2.setPixmap(pix)
        self.label_imgplanlong_2.setScaledContents(True)  # 让图片自适应label大小

        ######################################################################
        pix = QPixmap(':/images/plan02.png')
        self.label_imgplan.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgplan.setPixmap(pix)
        self.label_imgplan.setScaledContents(True)  # 让图片自适应label大小

        self.label_imgplan_2.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgplan_2.setPixmap(pix)
        self.label_imgplan_2.setScaledContents(True)  # 让图片自适应label大小

        self.label_imgplan_3.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgplan_3.setPixmap(pix)
        self.label_imgplan_3.setScaledContents(True)  # 让图片自适应label大小

        ######################################################################
        pix = QPixmap(':/images/car01.png')
        self.label_imgboard.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgboard.setPixmap(pix)
        self.label_imgboard.setScaledContents(True)  # 让图片自适应label大小

        self.label_imgboard_2.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgboard_2.setPixmap(pix)
        self.label_imgboard_2.setScaledContents(True)  # 让图片自适应label大小

        ######################################################################
        pix = QPixmap(':/images/car02.png')
        self.label_imggroup.resize(pix.width() * mark, pix.height() * mark)
        self.label_imggroup.setPixmap(pix)
        self.label_imggroup.setScaledContents(True)  # 让图片自适应label大小

        self.label_imggroup_2.resize(pix.width() * mark, pix.height() * mark)
        self.label_imggroup_2.setPixmap(pix)
        self.label_imggroup_2.setScaledContents(True)  # 让图片自适应label大小

        ######################################################################
        pix = QPixmap(':/images/convert.png')
        self.label_imgzhanqu.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgzhanqu.setPixmap(pix)
        self.label_imgzhanqu.setScaledContents(True)  # 让图片自适应label大小

        ######################################################################
        pix = QPixmap(':/images/commander.png')
        self.label_imgzhanqu_img.resize(pix.width() * mark, pix.height() * mark)
        self.label_imgzhanqu_img.setPixmap(pix)
        self.label_imgzhanqu_img.setScaledContents(True)  # 让图片自适应label大小

        ###########################设置按钮透明###########################################
        op01 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op01.setOpacity(0)
        self.pushButton.setGraphicsEffect(op01)

        op02 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op02.setOpacity(0)
        self.pushButton_2.setGraphicsEffect(op02)

        op03 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op03.setOpacity(0)
        self.pushButton_3.setGraphicsEffect(op03)

        ######################################################################
        self.pix_show = QPixmap(':/images/board.png')
        self.pix_show_choose = QPixmap(':/images/board_choose.png')
        self.label_imgshow01.resize(self.pix_show.width() * mark, self.pix_show.height() * mark)
        self.label_imgshow01.setPixmap(self.pix_show)
        self.label_imgshow01.setScaledContents(True)  # 让图片自适应label大小

        self.label_imgshow02.resize(self.pix_show.width() * mark, self.pix_show.height() * mark)
        self.label_imgshow02.setPixmap(self.pix_show)
        self.label_imgshow02.setScaledContents(True)  # 让图片自适应label大小

        self.label_imgshow03.resize(self.pix_show.width() * mark, self.pix_show.height() * mark)
        self.label_imgshow03.setPixmap(self.pix_show)
        self.label_imgshow03.setScaledContents(True)  # 让图片自适应label大小
        self.ChooseLabel(0)

        self.pushButton.clicked.connect(self.pushuBush01_click)
        self.pushButton_2.clicked.connect(self.pushuBush02_click)
        self.pushButton_3.clicked.connect(self.pushuBush03_click)

        # 创建遥信数据更新线程
        self.t1 = threading.Thread(target=self.updateSensorData, args=(self,))
        self.t1.start()

        self.m_bIsHand = False  # 使能摇杆
        # # 创建摇杆监测线程
        # t1 = threading.Thread(target=rocking_thread, args=(self,))
        # t1.start()

        self.actionenableHand.toggled.connect(self.toggleHand)
        self.actionenableVideo.toggled.connect(self.toggleVideo)
        self.actionenableSensor.toggled.connect(self.toggleSensor)

        threading.Thread(target=server_target, args=(self,)).start()  # 创建摇杆回调程序处理线程
        self.choose_device = 0

        self.label_sensor01.setText("")
        self.label_sensor02.setText("")
        self.label_sensor03.setText("")
        self.label_sensor04.setText("")
        self.label_sensor05.setText("")

    def toggleHand(self, state):
        if state:
            try:
                self.device = (hid.HidDeviceFilter(vendor_id=0x044F, product_id=0x0402).get_devices())[0]
            except Exception as e:
                print(e)
                print("未找到摇杆设备，请插入摇杆设备后重试")
                self.usbIsOpened = False
                return
            self.device.open()
            self.usbIsOpened=True
            # set custom raw data handler
            self.device.set_raw_data_handler(qtsample_handler)
        else:
            if self.usbIsOpened:
                self.device.close()
            else:
                print("请插入设备")

    def toggleVideo(self, state):
        if state:
            print("3")
        else:
            print("4")

    def toggleSensor(self, state):
        if state:
            self.enableSensor = True
        else:
            self.enableSensor = False
            self.label_sensor01.setText("")
            self.label_sensor02.setText("")
            self.label_sensor03.setText("")
            self.label_sensor04.setText("")
            self.label_sensor05.setText("")

    def pushuBush01_click(self):
        self.ChooseLabel(0)

    def pushuBush02_click(self):
        self.ChooseLabel(1)

    def pushuBush03_click(self):
        self.ChooseLabel(2)

    def ChooseLabel(self, marsk):
        if marsk < 0:
            marsk = 3
        elif marsk > 2:
            marsk = 0

        self.choose_device = marsk
        if marsk == 0:
            self.label_imgshow01.setPixmap(self.pix_show_choose)
            self.label_imgshow02.setPixmap(self.pix_show)
            self.label_imgshow03.setPixmap(self.pix_show)
        elif marsk == 1:
            self.label_imgshow01.setPixmap(self.pix_show)
            self.label_imgshow02.setPixmap(self.pix_show_choose)
            self.label_imgshow03.setPixmap(self.pix_show)
        else:
            self.label_imgshow01.setPixmap(self.pix_show)
            self.label_imgshow02.setPixmap(self.pix_show)
            self.label_imgshow03.setPixmap(self.pix_show_choose)

    def updateSensorData(self, _self):
        while 1:
            while self.enableSensor:
                value = modbusReadRist(SensorRigist01)
                # label1.setText("%s" % ("red", "helloworld"))  # 红色
                self.label_sensor01.setText("传感器01：" + str(value))
                value = modbusReadRist(SensorRigist02)
                self.label_sensor02.setText("传感器02：" + str(value))
                value = modbusReadRist(SensorRigist03)
                self.label_sensor03.setText("传感器03：" + str(value))
                value = modbusReadRist(SensorRigist04)
                self.label_sensor04.setText("传感器04：" + str(value/10.0))
                value = modbusReadRist(SensorRigist05)
                self.label_sensor05.setText("传感器05：" + str(value/10.0))
                sleep(0.1)
            sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_motor = Gis_Form()

    ui_motor.show()
    sys.exit(app.exec_())
