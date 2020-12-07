
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


# /usr/bin/python
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
