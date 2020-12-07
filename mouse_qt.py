import json
import socket
import threading

from time import sleep
from msvcrt import kbhit
import pywinusb.hid as hid

from modbusMaster import modbusSetABS, REGIST_ABSX01, modbusWriteRist, DORigest01_01, REGIST_ABSY02, REGIST_ABSY01, \
    REGIST_ABSX02, DORigest02_01

g_CurrentX = 128
g_CurrentY = 128
g_Short = False

counter = 0

g_last_CurrentX = 0
g_last_CurrentY = 0
g_last_Short = 0
is_initial_value = False
g_bScondEnable = False  # 使能云台二

g_changeFlag = False  # 延时判断按键按下
g_counter_hand = 0
g_lastValue = 0


# 处理UDP服务器接收到的数据
def qtsample_handler_(_self, data):
    global g_CurrentX
    global g_CurrentY
    global g_Short
    global g_last_CurrentX
    global g_last_CurrentY
    global g_last_Short
    global is_initial_value

    # print(data)

    g_CurrentX = data[5]
    g_CurrentY = data[7]
    nowShort = 0
    if data[1] == 1 or data[1] == 33:
        nowShort = 1
    else:
        nowShort = 0
    if nowShort != g_Short:
        g_Short = nowShort
        if _self.choose_device == 0:
            modbusWriteRist(DORigest01_01, g_Short)
        else:
            modbusWriteRist(DORigest02_01, g_Short)

    # print(g_CurrentY, g_CurrentX, g_Short)
    global counter
    global messageID
    global g_role
    counter = counter + 1
    if counter > 10:
        counter = 0
        v_x = int(g_CurrentX / 10)
        v_y = int(g_CurrentY / 10)
        if not is_initial_value:  # 首次进行初始化
            g_last_CurrentX = v_x
            g_last_CurrentY = v_y
            g_last_Short = 0
            is_initial_value = True
            return
        if v_x - g_last_CurrentX != 0:
            value = v_x - g_last_CurrentX
            if _self.choose_device == 0:
                modbusSetABS(REGIST_ABSX01, value)
            else:
                modbusSetABS(REGIST_ABSX02, value)
            print("set X" + str(value))
        if v_y - g_last_CurrentY != 0:
            value = v_y - g_last_CurrentY
            if _self.choose_device == 0:
                modbusSetABS(REGIST_ABSY01, -value)
            else:
                modbusSetABS(REGIST_ABSY02, -value)
            print("set Y" + str(value))

    if data[2] == 4 or data[2] == 8 or data[2] == 16 or data[2] == 32:
        global g_changeFlag
        global g_counter_hand
        global g_lastValue
        if g_changeFlag:
            g_counter_hand = g_counter_hand + 1
            if g_counter_hand > 20:
                g_changeFlag = False
                g_counter_hand = 0
                if data[2] == g_lastValue:
                    if data[2]==4 or data[2]==8:
                        _self.ChooseLabel(_self.choose_device + 1)
                    else:
                        _self.ChooseLabel(_self.choose_device -1)
        else:
            g_changeFlag = True
            g_lastValue = data[2]

    # sleep(0.1)
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# client 发送端

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP = "127.0.0.1"
PORT = 23596


# UDP服务器接收线程
def server_target(param):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (IP, PORT)
    server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
    # server_socket.settimeout(10)  # 设置一个时间提示，如果10秒钟没接到数据进行提示

    while True:
        # 正常情况下接收数据并且显示，如果10秒钟没有接收数据进行提示（打印 "time out"）
        # 当然可以不要这个提示，那样的话把"try:" 以及 "except"后的语句删掉就可以了
        try:
            receive_data, client = server_socket.recvfrom(1024)
            data = receive_data.decode()  # 解码
            data = data.split(",")  # 分隔
            data = list(map(int, data))  # 转换
            qtsample_handler_(param, data)
        except socket.timeout:  # 如果10秒钟没有接收数据进行提示（打印 "time out"）
            print("tme out")


server_address = (IP, PORT)  # 接收方 服务器的ip地址和端口号


# 摇杆回调函数，通过UDP把数据发送到处理线程
def qtsample_handler(data):
    msg = ','.join(str(i) for i in data)
    client_socket.sendto(msg.encode(), server_address)  # 将msg内容发送给指定接收方


def rocking_thread(param):
    while not param.m_bIsHand:
        sleep(1)
    try:
        device = (hid.HidDeviceFilter(vendor_id=0x044F, product_id=0x0402).get_devices())[0]
    except Exception as e:
        print(e)
        print("未找到摇杆设备，请插入摇杆设备后重试")
        exit(0)

    threading.Thread(target=server_target, args=(param,)).start()  # 创建摇杆回调程序处理线程

    device.open()
    # set custom raw data handler
    device.set_raw_data_handler(qtsample_handler)
    print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
    while not kbhit() and device.is_plugged():
        # just keep the device opened to receive events
        sleep(0.5)
        if not param.isRuning:
            return
    device.close()
    return


if __name__ == "__main__":
    rocking_thread(1)

