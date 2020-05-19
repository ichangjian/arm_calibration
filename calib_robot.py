#!/usr/bin/python3

# import calib_device
import socket
import time
import os


class Robot():
    def __init__(self, device):
        self.conn = None
        self.device = device
        self.file_fergb_name = ['0', '0000033330000', '0000066660000', '0000100000000', '0000133330000', '0000166660000', '0000200000000', '0000233330000', '0000266660000', '0000300000000',
                                '0000333330000', '0000366660000', '0000400000000', '0000433330000', '0000466660000', '0000500000000', '0000533330000']

    def __del__(self):
        if not self.conn is None:
            self.conn.close()

    def init_socket(self, ip, port):
        sk = socket.socket()
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.bind((ip, port))
        sk.listen(5)
        conn, address = sk.accept()

        ret = str(conn.recv(1024), encoding="utf-8")
        print("接收到设备数据" + ret)
        time.sleep(0.1)
        conn.sendall(bytes("cstwo", encoding="utf-8"))
        print("已发送锁存校验数据")
        time.sleep(0.1)
        ret = str(conn.recv(1024), encoding="utf-8")
        print(ret)
        print("Socket通讯建立")
        self.conn = conn

    # 机械臂返回值确定
    def error_dct(self, rec, comm):
        if rec != comm:
            print('机械臂返回错误，请检查后重试')
            exit()

    def move_arm_stereoimu(self, data_save_path, log=[]):
        # 获取标定数据-初始化socket套接字
        conn = self.conn
        # 获取标定数据-P2S1S-IMU-FE内外参标定准备
        conn.sendall(bytes("P3S1S", encoding="utf-8"))
        print("准备移动到机械臂IMU-FE内外参标定点")
        time.sleep(1)
        ret = str(conn.recv(1024), encoding="utf-8")
        print(ret)
        self.error_dct(ret, 'P3S1E')
        print("已移动到机械臂IMU-FE内外参标定点，开始采集")
        time.sleep(1)
        self.device.capture_command_stereoimu_start()
        log.append(ret)
        conn.sendall(bytes("P2S1S", encoding="utf-8"))
        print("准备移动机械臂")

        # 获取标定数据-P2S1S-IMU-FE内外参标定
        ret = str(conn.recv(1024), encoding="utf-8")
        print(ret)
        if ret != 'P2S1E':
            exit()
        self.device.capture_command_stereoimu_stop()
        print('数据已保存')

        self.device.pull_stereoimu_data(data_save_path)

    def move_arm_fergb(self, fe_save_path, rgb_save_path, log=[]):
        # 获取标定数据-P3-静态内外参标定
        conn = self.conn
        conn.sendall(bytes("P3S1S", encoding="utf-8"))
        print("准备移动到下一个点")

        x = 1
        while (x < 16):
            ret = str(conn.recv(1024), encoding="utf-8")
            print(ret)
            print("已移动到机械臂静态内外参标定点，开始标定")
            print('P3位置' + str(x) + '数据开始采集')
            self.device.capture_command_fergb()
            self.device.pull_fe_data(os.path.join(
                fe_save_path, self.file_fergb_name[x]))
            self.device.pull_rgb_data(os.path.join(
                rgb_save_path, self.file_fergb_name[x]))
            print('P3位置' + str(x) + '数据已保存')
            if x < 10:
                senddata = "P3S" + str(x) + "S"
            if x > 9:
                senddata = "3S" + str(x) + "S"
            conn.sendall(bytes(senddata, encoding="utf-8"))
            print("准备移动到下一个点")
            time.sleep(0.5)
            x = x + 1
        ret = str(conn.recv(1024), encoding="utf-8")
        print(ret)

    def move_arm_imu(self, log=[]):
        conn = self.conn

        # 获取标定数据-P1S1S-IMU标定步骤1
        imu_result = 1
        while (imu_result):
            step = 1
            while (step < 7):
                conn.sendall(bytes("P4S" + str(step) + "S", encoding="utf-8"))
                print("已发送下一点位置数据")
                time.sleep(0.1)
                ret = str(conn.recv(1024), encoding="utf-8")
                print(ret)
                print("已移动到机械臂IMU标定" + str(step) +
                      "号点，开始" + str(step) + "位置标定")
                time.sleep(14)
                f = os.popen(r"python c_l.py capimu", "r")
                shuchu = f.read()
                f.close()
                print(shuchu)
                time.sleep(2)
                f = os.popen(r"python c_l.py stopcapimu", "r")
                shuchu = f.read()
                f.close()
                print(shuchu)
                f = os.popen(
                    r"mv /run/user/1000/gvfs/smb-share:server=192.168.0.3,share=buff/cam-imu/imu0.csv imu/" + no[
                        step - 1], "r")
                f.close()
                f = os.system("./imucal 1 imu/" + no[step - 1])
                print(f)
                '''
                n=2
                while(shuchu[0]!='0'):
                    print('标定失败，进行第['+str(n)+']次尝试')
                    f = os.popen(r"adb shell testimucal "+str(step), "r")
                    shuchu = f.read()
                    f.close()
                    n=n+1
                    if n>6:
                        print('6次标定都失败，请注意是不是夜深人静，再进行重试')
                        conn.sendall(bytes("GHOME",encoding="utf-8"))
                        print("准备移动到装配点")
                        time.sleep(1)
                        ret = str(conn.recv(1024),encoding="utf-8")
                        print(ret)
                        cali.error_dct(ret,'HOMED')
                        conn.close()
                        exit()
                '''
                print("IMU标定" + str(step) + "结果" + shuchu)
                step = step + 1
                print("准备移动到下一个点")
            f = os.system(r"./imucal 2 imu/")
            print(f)
            imu_result = 0

        f = os.popen(
            r"rm -r /run/user/1000/gvfs/smb-share:server=192.168.0.3,share=buff/cam-imu", "r")
        f.close()
        conn.sendall(bytes("GHOME", encoding="utf-8"))
        print("准备移动到装配点")
        time.sleep(1)

        # 等待设备到装配点,安装设备
        ret = str(conn.recv(1024), encoding="utf-8")
        print(ret)
        self.error_dct(ret, 'HOMED')
        print('IMU标定完成')
        # os.system('adb pull /data/hmdinfo/AccelBias.txt')
        os.chdir(self.selected_path)
        self.content.append('IMU标定完成')
        # conn.close()