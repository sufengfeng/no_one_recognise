# encoding: utf-8
from time import sleep

import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
# /usr/bin/python
import configparser

SensorRigist01 = 64
SensorRigist02 = 65
SensorRigist03 = 66
SensorRigist04 = 94
SensorRigist05 = 95
Sensorauto = 57

REGIST_SPEEDX01 = 26
REGIST_SPEEDY01 = 27
REGIST_ABSX01 = 28
REGIST_ABSY01 = 29
REGIST_ABSX_R01 = 30
REGIST_ABSY_R01 = 31

REGIST_SPEEDX02 = 32
REGIST_SPEEDY02 = 33
REGIST_ABSX02 = 34
REGIST_ABSY02 = 35
REGIST_ABSX_R02 = 36
REGIST_ABSY_R02 = 37

DORigest01_01 = 90
DORigest01_02 = 91
DORigest01_03 = 92
DORigest01_04 = 93

DORigest02_01 = 94
DORigest02_02 = 95
DORigest02_03 = 96
DORigest02_04 = 97

master = ""

Marviw_IP = ""
Marviw_Port = 0

CameraIP = ""
CameraPort = ""
CameraUserName = ""
CameraPassword = ""


def InitGlobalParam():
    global Marviw_IP
    global Marviw_Port

    global CameraIP
    global CameraPort
    global CameraUserName
    global CameraPassword

    cf = configparser.ConfigParser()
    cf.read("configure.conf")
    print(cf.sections())
    print(cf.options("db"))

    Marviw_IP = cf.get("db", "marviw_ip")

    Marviw_Port = cf.getint("db", "marviw_port")

    CameraIP = cf.get("db", "cameraip")
    CameraPort = cf.getint("db", "cameraport")
    CameraUserName = cf.get("db", "camerausername")
    CameraPassword = cf.get("db", "camerapassword")
    print(Marviw_IP, Marviw_Port, CameraIP, CameraPort)


g_KeyData = [1, 0, 32, 0, 4, 15, 0, 2, 0, 2, 0, 2, 255, 63, 255, 63, 130, 240, 128, 240, 129, 72, 195, 39, 197, 57, 8,
             2, 0, 0, 0, 0, 0, 0, 0, 0]


def init_modbus():
    global master
    global Marviw_IP
    global Marviw_Port
    try:
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)
    except Exception as e:
        print(e)
        print("连接到RTE 错误")
        print(Marviw_IP)
        print(Marviw_Port)
        exit(0)


def modbusSetABS(regest, addValue):
    global master
    try:
        Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=regest + 2,
                                    quantity_of_x=1,
                                    output_value=0)
    except Exception as e:
        print(e)
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)
        return
    print(Hold_value)
    value = Hold_value[0]
    if value > 32768:
        value = value - 65536
    value = value + addValue
    try:
        Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=regest,
                                    quantity_of_x=1,
                                    output_value=value)
    except Exception as e:
        print(e)
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)
        return
    print(Hold_value)


def modbusReadRist(rigest):
    global master
    global Marviw_IP
    global Marviw_Port
    ip = Marviw_IP
    port = Marviw_Port
    value = 0
    try:
        # master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        # # master = mt.TcpMaster(ip, port)
        # master.set_timeout(5.0)
        Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=rigest,
                                    quantity_of_x=1,
                                    output_value=0)
    except Exception as e:
        print(e)
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)
        return value
    print(Hold_value)
    value = Hold_value[0]
    return value


def modbusWriteRist(rigest, value):
    global master
    global Marviw_IP
    global Marviw_Port
    try:
        Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=rigest,
                                    quantity_of_x=1,
                                    output_value=value)
    except Exception as e:
        print(e)
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)
        return
    print(Hold_value)
    value = Hold_value[0]


if __name__ == '__main__':
    pass
    # sendToSlave(1)
