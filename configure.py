# /usr/bin/python
import configparser

cf = configparser.ConfigParser()
cf.read("configure.conf")


Marviw_IP = cf.get("INI", "Marviw_IP")
Marviw_Port = cf.getint("INI", "Marviw_Port")

Barracks_IP = cf.get("INI", "Barracks_IP")
Theaters_IP = cf.get("INI", "Theaters_IP")
Headquarters_IP = cf.get("INI", "Marviw_IP")

Slave_PORT = cf.getint("INI", "Slave_PORT")
Master_PORT = cf.getint("INI", "Master_PORT")
g_role = cf.getint("INI", "g_role")

CameraIP = cf.get("INI", "CameraIP")
CameraPort = cf.getint("INI", "CameraPort")
CameraUserName = cf.get("INI", "CameraUserName")
CameraPassword = cf.get("INI", "CameraPassword")



g_KeyData = [1, 0, 32, 0, 4, 15, 0, 2, 0, 2, 0, 2, 255, 63, 255, 63, 130, 240, 128, 240, 129, 72, 195, 39, 197, 57, 8,
             2, 0, 0, 0, 0, 0, 0, 0, 0]
