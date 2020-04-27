import sys
import datetime
import os
import socket
import sys
import time



print (sys.argv[1])
client = socket.socket()
ip_port = ('localhost', 7081)
client.connect(ip_port)


client.sendall(bytes(sys.argv[1],encoding="utf-8"))
from_server_msg = client.recv(1024)
print(from_server_msg)



client.close()