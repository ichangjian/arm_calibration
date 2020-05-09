# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 17:35:53 2018

@author: Eric
"""

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


class calibration(QWidget):

    def __init__(self, parent=None):
        super(calibration, self).__init__(parent)
        layout = QVBoxLayout()

        with open('calib_profile.json', 'r') as f:
            config = json.load(f)
        self.config = config
 
        self.label_1 = QLabel()
        self.label_1.setText("状态显示")
        layout.addWidget(self.label_1)
        self.setWindowTitle("Calibration For G2")

        self.content = QTextBrowser()
        layout.addWidget(self.content)

        self.label_2 = QLabel()
        self.label_2.setText("工厂标定 版本1.1")
        layout.addWidget(self.label_2)

        self.btn_f1b = QPushButton()
        self.btn_f1b.clicked.connect(self.select_path)
        self.btn_f1b.setText("1.选定工作目录")
        layout.addWidget(self.btn_f1b)

        self.btn_f2 = QPushButton()
        self.btn_f2.clicked.connect(self.cv_data_capture)
        self.btn_f2.setText("2.CV标定（FE+RGB+IMU）")
        layout.addWidget(self.btn_f2)

        self.btn_f3 = QPushButton()
        self.btn_f3.clicked.connect(self.cali_imu)
        self.btn_f3.setText("3.IMU自身标定")
        layout.addWidget(self.btn_f3)

        self.btn_f4 = QPushButton()
        self.btn_f4.clicked.connect(self.file_value)
        self.btn_f4.setText("4.标定文件比对")
        layout.addWidget(self.btn_f4)

        self.label_3 = QLabel()
        self.label_3.setText("调试功能")
        layout.addWidget(self.label_3)

        self.btn_1 = QPushButton()
        self.btn_1.clicked.connect(self.read_ID)
        self.btn_1.setText("Read Device ID")
        layout.addWidget(self.btn_1)

        self.btn_1a = QPushButton()
        self.btn_1a.clicked.connect(self.adb_reboot)
        self.btn_1a.setText("reboot")
        layout.addWidget(self.btn_1a)

        self.btn_1b = QPushButton()
        self.btn_1b.clicked.connect(self.cal_stereo_imu)
        self.btn_1b.setText("计算CV参数")
        layout.addWidget(self.btn_1b)

        self.btn_2 = QPushButton()
        self.btn_2.clicked.connect(self.cali_slam_s)
        self.btn_2.setText("SLAM标定开始抓图")
        layout.addWidget(self.btn_2)

        self.btn_3 = QPushButton()
        self.btn_3.clicked.connect(self.cali_slam_e)
        self.btn_3.setText("SLAM标定结束抓图")
        layout.addWidget(self.btn_3)

        self.btn_5 = QPushButton()
        self.btn_5.clicked.connect(self.select_save_path)
        self.btn_5.setText("选择保存路径")
        layout.addWidget(self.btn_5)
    
        self.btn_4 = QPushButton()
        self.btn_4.clicked.connect(self.FE_capture_one)
        self.btn_4.setText("FE抓图")
        layout.addWidget(self.btn_4)

        self.btn_6 = QPushButton()
        self.btn_6.clicked.connect(self.RGB_capture_one)
        self.btn_6.setText("RGB抓图")
        layout.addWidget(self.btn_6)

        if (self.config["Enviroment"]["TOF_set"]):
            self.btn_7 = QPushButton()
            self.btn_7.clicked.connect(self.IR_capture_one)
            self.btn_7.setText("IR抓图")
            layout.addWidget(self.btn_7)
        
        if (self.config["Enviroment"]["TOF_dump_set"]):
            self.btn_8 = QPushButton()
            self.btn_8.clicked.connect(self.TOF_dump_file)
            self.btn_8.setText("TOF抓图")
            layout.addWidget(self.btn_8)

        self.setLayout(layout)


        self.kalibr_path = "/home/"+getpass.getuser()+"/new_G2/calib-template/"
        self.back_path = "/home/"+getpass.getuser()+"/server/"
        self.dutpath = '/storage/emulated/0/Android/data/com.tmac.camerapreview/files'
        self.no = ['0', '0000033330000', '0000066660000', '0000100000000', '0000133330000', '0000166660000', '0000200000000', '0000233330000', '0000266660000', '0000300000000',
                   '0000333330000', '0000366660000', '0000400000000', '0000433330000', '0000466660000', '0000500000000', '0000533330000']
        self.no2 = ['0',' ']
        self.device_ID = ' '
        self.save_path = ' '
        self.selected_path = ' '

    def push_app(self):
        log = cali.read_hmd_id()
        os.system('adb install '+self.config["Enviroment"]["RGB_capture_app"])
        self.content.append('当前设备ID为'+log)
    
    def test(self):
        print(self.kalibr_path)

    def adb_reboot(self):
        os.system('adb reboot')
        self.content.append('reboot device, waiting')

    def select_path(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "choose directory", "")
        self.selected_path = dir_path
        self.content.append('当前选择目录为：'+self.selected_path)
        #mod_time1=time.ctime(os.stat("calibration.py").st_mtime)
        #mod_time2=time.ctime(os.stat("cali.py").st_mtime)
        #self.content.append('当前标定程序日期为：'+mod_time1+'与'+mod_time2)

    def yaml_test(self):
        cali.yaml_process()
        time.sleep(1)
        cali.kalibr_RGB_FE(self.kalibr_path)
        time.sleep(1)
        cali.write_cali_para()
        os.chdir(self.selected_path)        

    def cv_data_capture(self):
        phase = 1
        phase2 = 1
        '''log = cali.read_ID()
        self.content.append('当前设备ID为'+log)
        log = cali.read_hmd_id()'''
        log = "HMD88888"
        self.content.append('当前设备头端ID为'+log)
        path = self.selected_path + '/' + log + '/'
        path2 = self.selected_path + '/' + log
        cali.data_file_creat(path)
        os.chdir(path)
        os.system('mkdir cam0')
        os.system('mkdir CVIMG')
        os.system('cp /home/cv/new_G2/c_l.py c_l.py')
        self.content.append('当前工作目录切换到：'+path)
        self.save_path = path
        print(self.save_path)

        print(datetime.datetime.now())
        time.sleep(0.1)
        state = 'error'
        while (state!='ok'):
            #获取标定数据-初始化socket套接字
            sk = socket.socket()
            sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            sk.bind(("192.168.0.10",7080))
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

            #获取标定数据-P2S1S-IMU-FE内外参标定
            ret = str(conn.recv(1024),encoding="utf-8")
            print(ret)
            if ret != 'P2S1E': exit()
            print(self.save_path)
            log = cali.imu_fe_capture_end(self.save_path)
            self.content.append(log)
            print('数据已保存') 

            if phase == 1 :
                #获取标定数据-P3-静态内外参标定
                conn.sendall(bytes("P3S1S",encoding="utf-8"))
                print("准备移动到下一个点")
                time.sleep(1)
                '''
                os.system('mkdir TOF')
                path_TOF = path+'TOF/'
                os.chdir(path_TOF)
                os.system('cp '+self.kalibr_path+'irconvert irconvert')
                os.chdir(path)
                '''
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
                #os.system('rm TOF/irconvert')

            #结束标定，回到初始位置 
            time.sleep(1)
            conn.sendall(bytes("P3S1S",encoding="utf-8"))
            print("准备移动到装配点")
            time.sleep(1)
            ret = str(conn.recv(1024),encoding="utf-8")
            print(ret)
            cali.error_dct(ret,'P3S1E')
            time.sleep(2)
            print(datetime.datetime.now())
            print('数据已保存')
            print('标定获取数据结束')
            self.content.append('开始计算标定数据')

            #标定数据计算开始
            if phase2 == 1 :
                os.chdir(self.save_path)
                '''
                os.system('adb pull /data/hmdinfo/rgb_display_transform.json')
                os.system('adb pull /data/hmdinfo/glass_profile.json')
                os.system('adb pull /data/hmdinfo/g2_glass_config.txt')
                '''
                print('开始执行参数计算')
                cali.calculate_IMU_FE(self.kalibr_path)
                state = cali.yaml_process()
                time.sleep(1)
                cali.kalibr_RGB_FE(self.kalibr_path)
                time.sleep(1)
                os.system('mv cam-imu cam-imu-2')
                os.system('mkdir cam-imu')
                os.system('cp -r CVIMG cam-imu/cam1')
                #os.system('mv TOF cam-imu/cam0')
                os.system('cp '+self.kalibr_path+'cameraindex.csv cam-imu/cameraindex.csv')
                #os.system('./kal_rgb.sh')
                #os.system('mv camchain-glasses.yaml rgb_tof.yaml')
                #cali.write_cv_para()
                os.chdir(self.selected_path)
                os.system('cp -r '+path2+' '+self.back_path)
        conn.close()
        print('CV标定已完成')
        self.content.append('CV系统标定已完成')        


    def cali_imu(self):
        log = cali.read_ID()
        self.device_ID = log
        self.content.append('当前设备ID为'+log)
        log = cali.read_hmd_id()
        print(log)
        self.content.append('当前设备头端ID为'+log)
        path = self.selected_path + '/' + log + '/'
        os.chdir(path)
        self.content.append('当前工作目录切换到：'+path)
        self.content.append('开始进行IMU标定')

        #获取标定数据-初始化socket套接字
        sk = socket.socket()
        sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sk.bind(("192.168.0.1",7080))
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

        #获取标定数据-P1S1S-IMU标定步骤1
        step = 1
        while (step<7) :   
            conn.sendall(bytes("P4S"+str(step)+"S",encoding="utf-8"))
            print("已发送下一点位置数据")
            time.sleep(0.1)
            ret = str(conn.recv(1024),encoding="utf-8")
            print(ret)
            print("已移动到机械臂IMU标定"+str(step)+"号点，开始"+str(step)+"位置标定")
            time.sleep(14)
            f = os.popen(r"adb shell testimucal "+str(step), "r")
            shuchu = f.read()
            f.close()
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
            print("IMU标定"+str(step)+"结果"+shuchu)
            step=step+1
            print("准备移动到下一个点")       
        
        conn.sendall(bytes("GHOME",encoding="utf-8"))
        print("准备移动到装配点")
        time.sleep(1)  
        
        #等待设备到装配点,安装设备
        ret = str(conn.recv(1024),encoding="utf-8")
        print(ret)
        cali.error_dct(ret,'HOMED')
        print('IMU标定完成')
        os.system('adb pull /data/hmdinfo/AccelBias.txt')
        os.chdir(self.selected_path)
        self.content.append('IMU标定完成')
        conn.close()

    
    def read_ID(self):
        log = cali.read_ID()
        self.content.append('当前设备ID为'+log)
        log = cali.read_hmd_id()
        self.device_ID = log
        self.content.append('当前设备头端ID为'+log)

    def creat_dir(self):
        log = cali.read_ID()
        self.content.append('当前设备ID为'+log)
        dir_path = QFileDialog.getExistingDirectory(
            self, "choose directory", "C:\\")
        self.content.append('当前选择目录为：'+dir_path)
        path = dir_path + '/' + log + '/'
        cali.data_file_creat(path)
        os.chdir(path)
        self.content.append('当前工作目录切换到：'+path)
        self.save_path = path
        print(self.save_path)

    def cali_slam_s(self):
        log = cali.imu_fe_capture_start()
        self.content.append(log)

    def cali_slam_e(self):
        print(self.save_path)
        log = cali.imu_fe_capture_end(self.save_path)
        self.content.append(log)

    def cal_stereo_imu(self):
        print(self.save_path)
        os.chdir(self.save_path)
        print('开始执行参数计算')
        cali.calculate_IMU_FE(self.kalibr_path)
        time.sleep(3)
        cali.yaml_process()
        os.chdir(self.selected_path)
        self.content.append('CV系统标定已完成') 

    def select_save_path(self):
        s_path = QFileDialog.getExistingDirectory(
            self, "choose directory", "")
        self.save_path = s_path+'/'
        self.content.append('当前选择目录为：'+self.save_path)
        os.chdir(self.save_path)

    def FE_capture_one(self):
        log = cali.FE_capture(self.save_path,'x',self.config["DevicePath"]["FE_path"],self.config["Command"]["FE_capture"])
        self.content.append(log)

    def RGB_capture_one(self):
        log = cali.RGB_capture(self.save_path,'x',self.config["DevicePath"]["RGB_path"],self.config["Command"]["RGB_capture"])
        self.content.append(log)

    def IR_capture_one(self):
        log = cali.TOF_IR_capture(self.save_path,'x',self.config["DevicePath"]["TOF_IR_path"],self.config["Command"]["TOF_IR_capture"])
        self.content.append(log)

    def TOF_dump_file(self):
        log = cali.TOF_dump(self.save_path,self.config["DevicePath"]["TOF_dump_path"],self.config["Command"]["TOF_dump_file"])
        self.content.append(log)
    
    def RGB_FE_cap(self):
        time.sleep(1)
        x = 1
        while (x<16) :
            print("已移动到机械臂静态内外参标定点，开始标定")
            cali.FE_capture(self.save_path,self.no[x])
            cali.RGB_capture(self.save_path,self.no[x])
            x=x+1

    def file_value(self):
        log = cali.read_ID()
        self.device_ID = log
        self.content.append('当前设备ID为'+log)
        log = cali.read_hmd_id()
        print(log)
        os.system('adb shell setprop debug.hmdinfo_backup.enable 1')
        self.content.append('当前设备头端ID为'+log)
        path = self.selected_path + '/' + log + '/'
        self.content.append('当前工作目录切换到：'+path)
        target_path = '/data/hmdinfo/'
        os.chdir(path)
        cali.write_cali_para()
        time.sleep(2)
        #os.system('adb shell rm '+target_path+'*')
        self.content.append('删除box端文件')
        time.sleep(1)
        os.system('adb shell input keyevent 135')
        self.content.append('读取头端到本地')
        time.sleep(8)
        os.system('adb pull '+target_path)
        self.content.append('当前比对路径:'+self.save_path)
        log=cali.file_compare('cam0_G2-sdm845.yaml','hmdinfo/cam0_G2-sdm845.yaml')
        self.content.append('cam0_G2-sdm845文件比对结果：'+log)
        log=cali.file_compare('cam1_G2-sdm845.yaml','hmdinfo/cam1_G2-sdm845.yaml')
        self.content.append('cam1_G2-sdm845文件比对结果：'+log)
        log=cali.file_compare('AccelBias.txt','hmdinfo/AccelBias.txt')
        self.content.append('AccelBias.txt文件比对结果：'+log)
        log=cali.file_compare('rgb_fe.yaml','hmdinfo/rgb_fe.yaml')
        self.content.append('rgb_fe.yaml文件比对结果：'+log)
        log=cali.file_compare('rgb_tof.yaml','hmdinfo/rgb_tof.yaml')
        self.content.append('rgb_fe.yaml文件比对结果：'+log)
        log=cali.file_compare('glass_profile.json','hmdinfo/glass_profile.json')
        self.content.append('glass_profile.json文件比对结果：'+log)
        log=cali.file_compare('rgb_display_transform.json','hmdinfo/rgb_display_transform.json')
        self.content.append('rgb_display_transfo rm.json文件比对结果：'+log)
        log=cali.file_compare('g2_glass_config.txt','hmdinfo/g2_glass_config.txt')
        self.content.append('g2_glass_config.txt文件比对结果：'+log)
        self.content.append('文件比对完成')
        os.chdir(self.selected_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calib = calibration()
    calib.show()
    sys.exit(app.exec_())
