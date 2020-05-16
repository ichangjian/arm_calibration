#!/usr/bin/python3
import cali
import os
import datetime
import socket
import time

shared_dir="/run/user/1000/gvfs/smb-share:server=192.168.0.3,share=buff"

stereoimu_dst_dir="stereoimu"
fergb_dst_dir="fergb"

stereoimu_src_dir="cam-imu"
fergb_src_dir="fergb"

s_ip="192.168.0.10"
s_port=7080

def get_device_ID():
    # return cali.read_ID()
    return "a"
    
def device_data_capture(work_path,log):
    """
    采集数据：双目+imu、FE+RGB、
    """
    id=get_device_ID()
    log.append('当前设备ID为'+id)
    
    data_path=work_path+"/"+id

    capture_stereoimu(data_path,log)
    capture_fergb(data_path,log)

def capture_stereoimu(data_path,log):
    stereoimu_path=os.path.join(data_path,stereoimu_dst_dir)
    
    if not os.path.exists(data_path):
        os.system("mkdir "+data_path)

    if os.path.exists(stereoimu_path):
        os.system("rm -r "+stereoimu_path)
    os.system("mkdir "+stereoimu_path)

    print(datetime.datetime.now())
    move_arm_stereoimu()
    pull_data("mv",os.path.join(shared_dir,stereoimu_src_dir),stereoimu_path)

def capture_fergb(data_path,log):
    fergb_path=os.path.join(data_path,fergb_dst_dir)
    
    if not os.path.exists(data_path):
        os.system("mkdir "+data_path)

    if os.path.exists(fergb_path):
        os.system("rm -r "+fergb_path)
    os.system("mkdir "+fergb_path)

    print(datetime.datetime.now())
    print(data_path)

def pull_data(command,src_path,dst_path):
    os.system(command+" "+src_path+" "+dst_path)
    print('拉取了stereoimu数据')
    pass

def send_command_stereoimu_start(log=[]):
    f=os.popen(r"python c_l.py capfeimu","r")
    shuchu = f.read()
    f.close()
    print(shuchu)
    time.sleep(1)
    return True

def send_command_stereoimu_stop(log=[]):
    f = os.popen(r"python c_l.py stopcapfeimu","r")
    shuchu = f.read()
    f.close()
    print(shuchu)
    time.sleep(1)
    return True

def get_conn(ip,port):
    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sk.bind((ip,port))
    sk.listen(5)
    conn,address = sk.accept()
    return conn

def move_arm_stereoimu(log=[]):
    #获取标定数据-初始化socket套接字
    conn=get_conn(s_ip,s_port)
    ret = str(conn.recv(1024),encoding="utf-8")
    print("接收到设备数据"+ret)
    time.sleep(0.1)
    conn.sendall(bytes("cstwo",encoding="utf-8"))
    print("已发送锁存校验数据")
    time.sleep(0.1)
    ret = str(conn.recv(1024),encoding="utf-8")
    print(ret)
    print("Socket通讯建立")

    #获取标定数据-P2S1S-IMU-FE内外参标定准备
    conn.sendall(bytes("P3S1S",encoding="utf-8"))
    print("准备移动到机械臂IMU-FE内外参标定点")
    time.sleep(1)
    ret = str(conn.recv(1024),encoding="utf-8")
    print(ret)
    cali.error_dct(ret,'P3S1E')
    print("已移动到机械臂IMU-FE内外参标定点，开始采集")
    time.sleep(1)
    send_command_stereoimu_start()
    log.append(ret)
    conn.sendall(bytes("P2S1S",encoding="utf-8"))
    print("准备移动机械臂")

    #获取标定数据-P2S1S-IMU-FE内外参标定
    ret = str(conn.recv(1024),encoding="utf-8")
    print(ret)
    if ret != 'P2S1E': exit()
    send_command_stereoimu_stop()
    conn.close()
    print('数据已保存') 

def move_arm_fergb(log=[]):
 #获取标定数据-P3-静态内外参标定
    conn=get_conn(s_ip,s_port)
    conn.sendall(bytes("P3S1S",encoding="utf-8"))
    print("准备移动到下一个点")

    x = 1
    while (x<16) :
        ret = str(conn.recv(1024),encoding="utf-8")
        print(ret)
        print("已移动到机械臂静态内外参标定点，开始标定")
        print('P3位置'+str(x)+'数据开始采集')
        cali.FE_capture(self.save_path,self.no[x],self.config["DevicePath"]["FE_path"],self.config["Command"]["FE_capture"])
        cali.RGB_capture(self.save_path,self.no[x],self.config["DevicePath"]["RGB_path"],self.config["Command"]["RGB_capture"])
        '''
        os.chdir(path_TOF)
        cali.TOF_IR_capture(path_TOF,self.no[x])
        os.system('./irconvert '+self.no[x]+'.bin'+' '+self.no[x]+'.jpg 0.2')
        os.system('rm '+self.no[x]+'.bin')
        os.chdir(path)
        '''
        print('P3位置'+str(x)+'数据已保存')
        if x<10 :
            senddata = "P3S"+str(x)+"S"
        if x>9 :
            senddata = "3S"+str(x)+"S"
        conn.sendall(bytes(senddata,encoding="utf-8"))
        print("准备移动到下一个点")
        time.sleep(0.5)
        x=x+1
    ret = str(conn.recv(1024),encoding="utf-8")
    print(ret)
    conn.close()