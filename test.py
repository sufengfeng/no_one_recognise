
# import logging
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# # 创建 handler 输出到文件
# handler = logging.FileHandler("file.log", mode='w')
# handler.setLevel(logging.INFO)
#
# # handler 输出到控制台
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
#
# # 创建 logging format
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# ch.setFormatter(formatter)
#
# # add the handlers to the logger
# logger.addHandler(handler)
# logger.addHandler(ch)
#
# logger.info("hello, guoweikuang")
# logger.debug("print to debug")
# logger.error("error logging")
# logger.warning("warning logging")
# logger.critical("critical logging")


#/usr/bin/python
# import configparser
#
# import string, os, sys
#
# cf = configparser.ConfigParser()
#
# cf.read("test.conf")
#
# # return all section
# secs = cf.sections()
# print('sections:', secs)
#
#
# opts = cf.options("db")
# print('options:', opts)
#
#
# kvs = cf.items("db")
# print('db:', kvs)
#
#
# # read by type
# db_host = cf.get("db", "db_host")
# db_port = cf.getint("db", "db_port")
# db_user = cf.get("db", "db_user")
# db_pass = cf.get("db", "db_pass")
#
# # read int
# threads = cf.getint("concurrent", "thread")
# processors = cf.getint("concurrent", "processor")
#
# print("db_host:", db_host)
#
# print("db_port:", db_port)
#
# print("db_user:", db_user)
#
# print("db_pass:", db_pass)
#
#
# print("thread:", threads)
#
# print("processor:", processors)
#
#
# # modify one value and write to file
# cf.set("db", "db_pass", "xgmtest")
# cf.write(open("test.conf", "w"))

# import modbus_tk.modbus_tcp as mt
# import modbus_tk.defines as md
#
# master = mt.TcpMaster("192.168.3.164", 502)
# master.set_timeout(5.0)
# Hold_value=""
# try:
#     Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=26,
#                                 quantity_of_x=1,
#                                 output_value=0)
# except Exception as e:
#     print(e)
# print(Hold_value)


import cv2, numpy
cam_addr = "rtsp://admin:123456@" + "192.168.3.172" + "/mpeg4cif"  # camera address
print(cam_addr)
cap = cv2.VideoCapture(cam_addr)

while 1:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (900, 529))
        cv2.imshow("img", frame)
        cv2.waitKey(1)
    else:
        print(ret)