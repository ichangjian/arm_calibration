import datetime
import os
import socket
import sys
import time
import getpass
import json

import numpy as np
import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QPushButton,
                             QTextBrowser, QVBoxLayout, QWidget)

import cali


#获取标定数据-初始化socket套接字
sk = socket.socket()
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sk.bind(('localhost',7081))
sk.listen(5)
conn,address = sk.accept()
ret = str(conn.recv(1024),encoding="utf-8")
print("接收到设备数据"+ret)
time.sleep(0.1)
conn.sendall(bytes("cstwo",encoding="utf-8"))
print("已发送锁存校验数据")
time.sleep(0.1)
ret = str(conn.recv(1024),encoding="utf-8")
print(ret)
print("Socket通讯建立")

f = os.popen(r"python c_l.py aaa", "r")
n = f.read()
f.close()
print (n)

#获取标定数据-P2S1S-IMU-FE内外参标定准备
conn.sendall(bytes("P3S1S",encoding="utf-8"))
print("准备移动到机械臂IMU-FE内外参标定点")
time.sleep(1)
ret = str(conn.recv(1024),encoding="utf-8")
print(ret)
cali.error_dct(ret,'P3S1E')
print("已移动到机械臂IMU-FE内外参标定点，开始采集")
time.sleep(1)
log = cali.imu_fe_capture_start()
self.content.append(log)
conn.sendall(bytes("P2S1S",encoding="utf-8"))
print("准备移动机械臂")

f = os.popen(r"python c_l.py aaa", "r")
n = f.read()
f.close()
print (n)

conn.close()
