# coding:utf-8
"""
Created on Fri Dec 14 17:35:53 2018

@author: Eric
"""

import datetime
import os
import socket
import time

import numpy as np
import yaml

# 机械臂返回值确定
def error_dct(rec, comm):
    if rec != comm:
        print('机械臂返回错误，请检查后重试')
        exit()


# 设备挂载
def device_mount():
    print(datetime.datetime.now())
    time.sleep(0.1)
    n = ''
    while (n != "remount succeeded\n"):
        f = os.popen(r"adb remount", "r")
        time.sleep(1)
        n = f.read()
        f.close()
    print("眼镜设备挂载成功")
    return '眼镜设备挂载成功'


def read_ID():
    print(datetime.datetime.now())
    f = os.popen(r"adb devices", "r")
    shuchu = f.read()
    f.close()
    # print(shuchu)
    s = shuchu.split("\n")   # 切割换行
    # print(s)
    new = [x for x in s if x != '']  # 去掉空''
    # print(new)
    devices = []  # 可能有多个手机设备，获取设备名称
    for i in new:
        dev = i.split('\tdevice')
        if len(dev) >= 2:
            devices.append(dev[0])
    if not devices:
        print("眼镜设备没连上,请连接手机重新执行")
        exit()
    else:
        print("当前手机设备:%s" % str(devices))
    return devices[0]


def read_hmd_id():
	print(datetime.datetime.now())
	f = os.popen(r"adb shell cat sys/fpga_eeprom/glass_id", "r")
	shuchu = f.read()
	print(shuchu)
	f.close()
	return shuchu[0:8]


def data_file_creat(path):
    path = path.strip()
    path = path.rstrip("/")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return '标定数据目录 '+path+' 创建成功'
    else:
        print(path+' 目录已存在')
        os.system('rm -r '+path)
        print('删除目录中')
        time.sleep(5)
        os.makedirs(path)
        return '标定数据目录 '+path+' 创建成功'


def init_socket():
	sk = socket.socket()
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


def calculate_IMU_FE(kalibrpath):
	time.sleep(1)
	os.system('mv slam_data_save cam-imu')
	os.system('cp '+kalibrpath+'kal-cde-stereo.sh kal_stereo.sh')	
	os.system('cp '+kalibrpath+'kal-cde-stereo-imu.sh kal_imu.sh')
	os.system('cp '+kalibrpath+'imu_lenovo.yaml imu_lenovo.yaml')
	os.system('cp '+kalibrpath+'april_6x6.yaml april_6x6.yaml')
	os.system('chmod a+x kal_imu.sh')
	os.system('chmod a+x kal_stereo.sh')
	print(datetime.datetime.now())
	os.system('./kal_stereo.sh')
	os.system('cp camchain-glasses.yaml stereo.yaml')
	f = open("stereo.yaml","r") 
	data = f.readlines() 
	f.close()
	data[1]='  cam_overlaps: []\n'
	n=0
	data1=''
	while(n<9):
		data1 = data1+data[n]
		n=n+1
	fnew = open("camchain-glasses.yaml", "w")
	fnew.write(data1)
	fnew.close()   
	os.system('./kal_imu.sh')
	print(datetime.datetime.now())


def yaml_process():
	f = open("results-imucam-glasses.txt","r")   #设置文件对象
	data = f.readlines()  #直接将文件中按行读到list里，效果与方法2一样
	f.close()             #关闭文件
	f1 = open(r"stereo.yaml")
	x1 = yaml.load(f1)     

	distor = data[46-1]
	distor = distor.split("[")
	distor = distor[1].split("]")
	distor = distor[0].split(",")

	focal=data[43-1]
	focal=focal.split("[")
	focal=focal[1].split("]")
	focal=focal[0].split(",")

	princ=data[44-1]
	princ=princ.split("[")
	princ=princ[1].split("]")
	princ=princ[0].split(",")

	if (data[24-1][2]=='-'):
		rotate1='['+data[24-1][2:13]+', '+data[24-1][14:25]+', '+data[24-1][26:37]+', '
	elif (data[24-1][2]==' '):
		rotate1='['+data[24-1][3:13]+', '+data[24-1][14:25]+', '+data[24-1][26:37]+', '		
	if (data[25-1][2]=='-'):
		rotate2='          '+data[25-1][2:13]+', '+data[25-1][14:25]+', '+data[25-1][26:37]+', '
	elif (data[25-1][2]==' '):
		rotate2='          '+data[25-1][3:13]+', '+data[25-1][14:25]+', '+data[25-1][26:37]+', '
	if (data[26-1][2]=='-'):
		rotate3='          '+data[26-1][2:13]+', '+data[26-1][14:25]+', '+data[26-1][26:37]+']'
	elif (data[26-1][2]==' '):
		rotate3='          '+data[26-1][3:13]+', '+data[26-1][14:25]+', '+data[26-1][26:37]+']'
	if (data[24-1][38]=='-'):
		trans='['+data[24-1][38:49]+', '+data[25-1][38:49]+', '+data[26-1][38:49]+']'
	elif (data[24-1][38]==' '):
		trans='['+data[26-1][39:49]+', '+data[25-1][38:49]+', '+data[26-1][38:49]+']'

	rotate=rotate1+'\n'+rotate2+'\n'+rotate3+'\n'

	timeshift=data[30-1]
	timeafter=float(timeshift)*1000
	timeafter=('%.1f'%timeafter)
	timeafter=timeafter+'e+06'

	x2=x1['cam1']['T_cn_cnm1']
	n=0
	while(n<4):
		m=0
		while(m<4):
			x2[n][m]=('%.8f'%x2[n][m])
			m=m+1		
		n=n+1

	rotate1='['+x2[0][0]+', '+x2[0][1]+', '+x2[0][2]+', '
	rotate2='          '+x2[1][0]+', '+x2[1][1]+', '+x2[1][2]+', '
	rotate3='          '+x2[2][0]+', '+x2[2][1]+', '+x2[2][2]+']'
	trans_s='['+x2[0][3]+', '+x2[1][3]+', '+x2[2][3]+']'              
	rotate_s=rotate1+'\n'+rotate2+'\n'+rotate3+'\n'

	write_data1='%YAML:1.0'+'\n\n'+'model_type: KANNALA_BRANDT'+'\n'+'camera_name: fisheye_cvmodule1'+'\n'+\
	'image_width: 640'+'\n'+'image_height: 400'+'\n\n'+'projection_parameters:'+'\n'+'   k2: '+str(distor[0])\
	+'\n'+'   k3:'+str(distor[1])+'\n'+'   k4:'+str(distor[2])+'\n'+'   k5:'+str(distor[3])+'\n'+'   mu: '+\
	str(focal[0])+'\n'+'   mv:'+str(focal[1])+'\n'+'   u0: '+str(princ[0])+'\n'+'   v0:'+str(princ[1])+'\n\n'+\
	'imu_image_t_offset: '+timeafter+'\n\n'+'# Extrinsic parameter between IMU and Camera\n'+\
	'extrinsicRotation: !!opencv-matrix'+'\n'+'   rows: 3'+'\n'+'   cols: 3'+'\n'+'   dt: d'+'\n'+'   data: '\
	+rotate+'\n'+'extrinsicTranslation: !!opencv-matrix'+'\n'+'   rows: 3'+'\n'+'   cols: 1'+'\n'+'   dt: d'+'\n'\
	+'   data: '+trans+'\n\n'+'# stereo parameters from cam0 to cam1\n'+'Stereo_R: !!opencv-matrix\n'+\
	'   rows: 3'+'\n'+'   cols: 3'+'\n'+'   dt: d'+'\n'+'   data: '+rotate_s+'\n'\
	+'Stereo_T: !!opencv-matrix'+'\n'+'   rows: 3'+'\n'+'   cols: 1'+'\n'+'   dt: d'+'\n'\
	+'   data: '+trans_s+'\n'

	distor = x1['cam1']['distortion_coeffs']
	focal= x1['cam1']['intrinsics']
	princ = [focal[2],focal[3]]

	x3=float(trans[1:12])
	x3=x3-float(x2[0][3])
	x3=('%.8f'%x3)
	trans="["+str(x3)+trans[12:50]
	print(trans)
		
	write_data2='%YAML:1.0'+'\n\n'+'model_type: KANNALA_BRANDT'+'\n'+'camera_name: fisheye_cvmodule1'+'\n'+\
	'image_width: 640'+'\n'+'image_height: 400'+'\n\n'+'projection_parameters:'+'\n'+'   k2: '+str(distor[0])\
	+'\n'+'   k3:'+str(distor[1])+'\n'+'   k4:'+str(distor[2])+'\n'+'   k5:'+str(distor[3])+'\n'+'   mu: '+\
	str(focal[0])+'\n'+'   mv:'+str(focal[1])+'\n'+'   u0: '+str(princ[0])+'\n'+'   v0:'+str(princ[1])+'\n\n'+\
	'imu_image_t_offset: '+timeafter+'\n\n'+'# Extrinsic parameter between IMU and Camera\n'+\
	'extrinsicRotation: !!opencv-matrix'+'\n'+'   rows: 3'+'\n'+'   cols: 3'+'\n'+'   dt: d'+'\n'+'   data: '\
	+rotate+'\n'+'extrinsicTranslation: !!opencv-matrix'+'\n'+'   rows: 3'+'\n'+'   cols: 1'+'\n'+'   dt: d'+'\n'\
	+'   data: '+trans+'\n'

	T1 = int(data[24-1][41:44])
	T2 = int(data[25-1][41:44])
	T3 = int(data[26-1][41:44])
	print(T1)
	print(T2)
	print(T3)
	if abs(T1-105)<=5:
		if abs(T2-10)<=10:
			if abs(T3-10)<=10:
				fnew = open("cam0_G2-sdm845.yaml", "w")
				fnew.write(write_data1)
				fnew.close()
				fnew = open("cam1_G2-sdm845.yaml", "w")
				fnew.write(write_data2)
				fnew.close()
				return 'ok'
	return 'error'


def kalibr_RGB_FE(kalibrpath):
	print('开始标定RGB-FE数据')
	print(datetime.datetime.now())
	os.system('mv cam-imu cam-imu-0')
	os.system('rm -r glasses.bag')
	time.sleep(5)
	os.system('mkdir cam-imu')
	os.system('cp -r CVIMG cam-imu/cam1')
	os.system('mv cam0 cam-imu/cam0')
	os.system('cp '+kalibrpath+'kal_rgb.sh kal_rgb.sh')
	os.system('cp '+kalibrpath+'cameraindex.csv cam-imu/cameraindex.csv')
	os.system('./kal_rgb.sh')
	print(datetime.datetime.now())
	print(datetime.datetime.now())
	print('计算RGB和IMU外参')

	#FE to RGB
	f1 = open(r"camchain-glasses.yaml")
	x1 = yaml.load(f1)
	data1=np.mat(np.zeros((4,4)))
	n=0
	while(n<4):
		m=0
		while(m<4):
			data1[n,m]=x1['cam1']['T_cn_cnm1'][n][m]
			m=m+1		
		n=n+1
	f1.close()

	#imu to FE
	f2 = open(r"camchain-imucam-glasses.yaml")
	x2 = yaml.load(f2)
	data2=np.mat(np.zeros((4,4)))
	n=0
	while(n<4):
		m=0
		while(m<4):
			data2[n,m]=x2['cam0']['T_cam_imu'][n][m]
			m=m+1		
		n=n+1
	f2.close()

	data3=np.dot(data1.I,data2.I)

	write_data="{\"Data\":["
	n=0
	while(n<3):
		m=0
		while(m<4):
			write_data=write_data+str(data3[n,m])+','
			m=m+1		
		n=n+1

	write_data=write_data+str(data3[3,0])+','+str(data3[3,1])+','+str(data3[3,2])+','+str(data3[3,3])+']}'
	print(write_data)
	fnew = open("rgbtoimu.txt", "w")
	fnew.write(write_data)
	fnew.close()
	os.system('mv camchain-glasses.yaml rgb_fe.yaml')


def write_cali_para():
	target_path = '/data/hmdinfo/'
	os.system('adb shell rm '+target_path+'*')
	print('写入标定数据到设备')  
	os.system('adb push rgbtoimu.txt '+target_path)
	os.system('adb push cam0_G2-sdm845.yaml '+target_path)
	os.system('adb push cam1_G2-sdm845.yaml '+target_path)
	os.system('adb push stereo.yaml '+target_path)
	os.system('adb push rgb_fe.yaml '+target_path)
	os.system('adb push rgb_tof.yaml '+target_path)
	os.system('adb push rgb_display_transform.json '+target_path)
	os.system('adb push glass_profile.json '+target_path)
	os.system('adb push g2_glass_config.txt '+target_path)
	os.system('adb push AccelBias.txt '+target_path)
	time.sleep(1)
	os.system('adb shell input keyevent 134')
	time.sleep(5)

def write_cv_para():
	target_path = '/data/hmdinfo/'
	os.system('adb shell rm '+target_path+'*')
	print('写入标定数据到设备')  
	os.system('adb push rgbtoimu.txt '+target_path)
	os.system('adb push cam0_G2-sdm845.yaml '+target_path)
	os.system('adb push cam1_G2-sdm845.yaml '+target_path)
	os.system('adb push stereo.yaml '+target_path)
	os.system('adb push rgb_fe.yaml '+target_path)
	os.system('adb push rgb_tof.yaml '+target_path)
	os.system('adb push rgb_display_transform.json '+target_path)
	os.system('adb push glass_profile.json '+target_path)
	os.system('adb push g2_glass_config.txt '+target_path)
	time.sleep(1)
	os.system('adb shell input keyevent 134')
	time.sleep(5)


def imu_fe_capture_start():
    print("已移动到机械臂IMU-FE内外参标定点，开始标定")
    os.system('adb shell rm -rf /sdcard/slam_data_save')
    time.sleep(1)
    os.system('adb shell setprop debug.fisheyeimu.data 4')
    time.sleep(1)
    foff = os.popen(r"adb shell slamclienttest", "r")
    time.sleep(1)
    return '已经开始采集图像，请稍候'


def imu_fe_capture_end(save_path):
    os.system('adb shell setprop debug.fisheyeimu.data 0')
    time.sleep(1)
    os.system('adb pull /sdcard/slam_data_save '+ save_path)
    time.sleep(1)
    os.system('mv '+save_path+'slam_data_save/imu.csv '+save_path+'slam_data_save/imu0.csv')
    os.system('mv '+save_path+'slam_data_save/loop.txt '+save_path+'slam_data_save/loop01.txt')
    print('数据已保存')
    return '数据已保存'


def FE_capture(save_path,file_name,dutpath,cmd):
	n = 'xx'
	while (n[0]!="0") :
		f = os.popen(cmd, "r")
		shuchu = f.read()
		f.close()
		print('log'+shuchu)
		log_info = 'crash'
		result = log_info in shuchu
		if result : 
			os.system('adb reboot')
			print('camera crash, 设备重启中请稍候')
			time.sleep(35)
		time.sleep(2)
		f = os.popen(r"adb shell ls "+dutpath, "r")
		n = f.read()
		f.close()
		if (n==''):
			n='no image'
		print(n)
	os.system('adb shell mv ' + dutpath + '0.png ' + dutpath + file_name+ '.png')
	time.sleep(0.1)
	os.system('adb pull ' + dutpath +' '+ save_path)
	time.sleep(0.1)
	os.system('adb shell rm -rf ' + dutpath)
	return 'FE抓图完成'

def RGB_capture(save_path,file_name,dutpath,cmd):
	n = 'xx'
	while (n[0]!="r") :
		os.system(cmd)
		time.sleep(2)
		f = os.popen(r"adb shell ls "+dutpath, "r")
		n = f.read()
		f.close()
		if (n==''):
			n='no image'
		print(n)
	os.system('adb shell mv '+dutpath+'rgbpic.png '+dutpath+file_name+'.png')
	time.sleep(0.1)
	os.system('adb pull '+ dutpath + ' '+save_path)
	time.sleep(0.1)
	os.system('adb shell rm -rf ' + dutpath)
	return 'RGB抓图完成'

def file_compare(file1,file2):
	f1 = open(file1,"r")
	data1 = f1.readlines()
	f1.close()
	f2 = open(file2,"r")
	data2 = f2.readlines()
	f2.close()
	if (data1==data2):
		return 'ok'
	if (data1!=data2):
		return 'error'

def TOF_IR_capture (save_path,file_name,dutpath,cmd):
	n = 'xx'
	while (n[0]!="t") :
		os.system(cmd)
		time.sleep(2)
		f = os.popen(r"adb shell ls "+dutpath, "r")
		n = f.read()
		f.close()
		if (n==''):
			n='no image'
		print(n)
	os.system('adb shell mv '+dutpath+'tof_depth_000001.raw '+dutpath+file_name+'.bin')
	time.sleep(0.1)
	os.system('adb pull '+ dutpath+file_name+'.bin'+' '+save_path)
	time.sleep(0.1)
	os.system('adb shell rm ' + dutpath+'*')  
	return 'IR抓图完成'

def TOF_dump (save_path,dutpath,cmd):
	n = 'xx'
	while (n[0]!="t") :
		os.system(cmd)
		time.sleep(2)
		f = os.popen(r"adb shell ls "+dutpath+"/depth/", "r")
		n = f.read()
		f.close()
		if (n==''):
			n='no image'
		print(n)
	time.sleep(0.1)
	os.system('adb pull '+ dutpath+' '+save_path)
	time.sleep(0.1)
	os.system('adb shell rm -r ' + dutpath+'*')  
	return 'TOF抓图完成'