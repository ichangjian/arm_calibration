import sys
import datetime
import os
import socket
import sys
import time


sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sk.bind(('localhost',7081))
sk.listen(5)
client = None


while 1:
    if client is None:
        conn,address = sk.accept()  # 因为设置了接收连接数为1，所以不需要放在循环中接收
    try:
        ret = str(conn.recv(1024),encoding="utf-8")
        data = ret+"ok"
        conn.sendall(bytes(data,encoding="utf-8"))
    except Exception :
        client = None

