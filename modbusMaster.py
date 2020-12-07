# encoding: utf-8
from time import sleep

import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md

from configure import Marviw_Port, Marviw_IP

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

DORigest01_01=90
DORigest01_02=91
DORigest01_03=92
DORigest01_04=93


DORigest02_01=94
DORigest02_02=95
DORigest02_03=96
DORigest02_04=97

# def sendToSlave(param):
#     global g_KeyData
#     # 远程连接到服务器端
#     master = mt.TcpMaster(Marviw_IP, Marviw_Port)
#     master.set_timeout(5.0)
#     value = {40, 30, 50, 60}
#     Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=26,
#                                 quantity_of_x=1,
#                                 output_value=150)
#     print(Hold_value)
#     Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=27,
#                                 quantity_of_x=1,
#                                 output_value=151)
#     print(Hold_value)
#     Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=28,
#                                 quantity_of_x=1,
#                                 output_value=60)
#     print(Hold_value)
#     Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=29,
#                                 quantity_of_x=1,
#                                 output_value=-360)
#     print(Hold_value)
#     sleep(0.1)

master = mt.TcpMaster(Marviw_IP, Marviw_Port)
master.set_timeout(5.0)


# 设置电机转动角度
def modbusSetSpeed(speedx, stepx, speedy, stepy):
    global master
    Hold_value = (0,)
    try:
        Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=REGIST_SPEEDX,
                                    quantity_of_x=1,
                                    output_value=speedx)
    except Exception as e:
        print(e)
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)

    print(Hold_value)
    try:
        Hold_value = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=REGIST_SPEEDY,
                                    quantity_of_x=1,
                                    output_value=speedy)
    except Exception as e:
        print(e)
        master = mt.TcpMaster(Marviw_IP, Marviw_Port)
        master.set_timeout(5.0)

    print(Hold_value)


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
        master.set_timeout(5.0)
    print(Hold_value)


def modbusReadRist(rigest):
    global master
    value = 0
    try:
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

def modbusWriteRist(rigest,value):
    global master

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

