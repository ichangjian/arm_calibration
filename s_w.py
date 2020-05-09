import sys
import datetime
import os
import socket
import sys
import time


sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sk.bind(("192.168.0.3",7081))
sk.listen(5)
client = None


while 1:
    if client is None:
        conn,address = sk.accept()  # 因为设置了接收连接数为1，所以不需要放在循环中接收
    try:
        ret = str(conn.recv(1024),encoding="utf-8")
        if ret == "capfeimu":
            f = os.popen(r".\capture_fe_imu  Y:\\", "r")
		    n = f.read()
		    f.close()
        if ret == "stopcapfeimu":
            f = os.popen(r".\stop_capture_fe_imu", "r")
		    n = f.read()
		    f.close()
        if ret == "capfe":
            f = os.popen(r".\capture_fe Y:\\fe.png", "r")
		    n = f.read()
		    f.close()
        if ret == "caprgb":
            f = os.popen(r".\capture_rgb Y:\\rgb.png", "r")
		    n = f.read()
		    f.close()
        if ret == "capimu":
            f = os.popen(r"capture_fe.exe save_name", "r")
		    n = f.read()
		    f.close()
        data = n +"ok"
        conn.sendall(bytes(data,encoding="utf-8"))
    except Exception, e:
        client = None

