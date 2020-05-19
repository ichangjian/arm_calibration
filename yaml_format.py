#!/usr/bin/python3
import sys
import yaml
import numpy

def open_yaml(file_yaml):
	try:
		return yaml.load(open(file_yaml),Loader=yaml.SafeLoader)
	except:
		print("can't open ",file_yaml)
		


def write_cam0_yaml(cam0_internal,cam0_distortion,imu_cam0_time,cam0_imu_transformation,cam0_cam1_transformation,description):
	clb_dir="."
	print("Save\t"+clb_dir+"/cam0.yaml")
	f = open(clb_dir+"/cam0.yaml", "w")

	f.write("%YAML:1.0\n")
	f.write("\n")
	f.write(description+"\n")
	f.write("\n")
	f.write("model_type: KANNALA_BRANDT\n")
	f.write("camera_name: camera\n")
	f.write("image_width: 640\n")
	f.write("image_height: 400\n")
	f.write("\n")

	f.write("projection_parameters:\n   k2: {0}\n   k3: {1}\n   k4: {2}\n   k5: {3}\n".
			format(cam0_distortion[0], cam0_distortion[1], cam0_distortion[2], cam0_distortion[3]))
	f.write("   mu: {0}\n   mv: {1}\n   u0: {2}\n   v0: {3}\n".
			format(cam0_internal[0], cam0_internal[1], cam0_internal[2], cam0_internal[3]))
	f.write("\n")

	f.write("imu_image_t_offset: {:.4e}\n".format(imu_cam0_time*1e9))
	f.write("\n")
	cam0_imu_transformation=[j for i in cam0_imu_transformation for j in i ]
	f.write("#Rotation from camera frame to imu frame, imu^R_cam\n")
	f.write("extrinsicRotation: !!opencv-matrix\n")
	f.write("   rows: 3\n")
	f.write("   cols: 3\n")
	f.write("   dt: d\n")
	f.write("   data: [ {0[0]}, {0[1]}, {0[2]},\n          {0[4]}, {0[5]}, {0[6]},\n          {0[8]}, {0[9]}, {0[10]}]\n".
			format(cam0_imu_transformation))
	f.write("#Translation from camera frame to imu frame, imu^T_cam\n")
	f.write("extrinsicTranslation: !!opencv-matrix\n")
	f.write("   rows: 3\n")
	f.write("   cols: 1\n")
	f.write("   dt: d\n")
	f.write("   data: [ {0[3]}, {0[7]}, {0[11]}]\n".
			format(cam0_imu_transformation))
	f.write("\n")
	cam0_cam1_transformation=[j for i in cam0_cam1_transformation for j in i ]

	f.write("#stereo parameters from cam0 to cam1\n")
	f.write("Stereo_R: !!opencv-matrix\n")
	f.write("   rows: 3\n")
	f.write("   cols: 3\n")
	f.write("   dt: d\n")
	f.write("   data: [ {0[0]}, {0[1]}, {0[2]},\n          {0[4]}, {0[5]}, {0[6]},\n          {0[8]}, {0[9]}, {0[10]}]\n".
			format(cam0_cam1_transformation))
	f.write("\n")
	f.write("Stereo_T: !!opencv-matrix\n")
	f.write("   rows: 3\n")
	f.write("   cols: 1\n")
	f.write("   dt: d\n")
	f.write("   data: [ {0[3]}, {0[7]}, {0[11]}]\n".
			format(cam0_cam1_transformation))
	f.write("\n")

	f.close()


def write_cam1_yaml(cam1_internal,cam1_distortion,imu_cam1_time,cam1_imu_transformation,description):
	clb_dir="."
	print("Save\t"+clb_dir+"/cam1.yaml")
	f = open(clb_dir+"/cam1.yaml", "w")


	f.write("%YAML:1.0\n")
	f.write("\n")    
	f.write(description+"\n")
	f.write("\n")
	f.write("model_type: KANNALA_BRANDT\n")
	f.write("camera_name: camera\n")
	f.write("image_width: 640\n")
	f.write("image_height: 400\n")
	f.write("\n")

	f.write("projection_parameters:\n   k2: {0}\n   k3: {1}\n   k4: {2}\n   k5: {3}\n".
			format(cam1_distortion[0], cam1_distortion[1], cam1_distortion[2], cam1_distortion[3]))
	f.write("   mu: {0}\n   mv: {1}\n   u0: {2}\n   v0: {3}\n".
			format(cam1_internal[0], cam1_internal[1], cam1_internal[2], cam1_internal[3]))
	f.write("\n")

	f.write("imu_image_t_offset: {:.4e}\n".format(imu_cam1_time*1e9))
	f.write("\n")
	cam1_imu_transformation=[j for i in cam1_imu_transformation for j in i ]

	f.write("#Rotation from camera frame to imu frame, imu^R_cam\n")
	f.write("extrinsicRotation: !!opencv-matrix\n")
	f.write("   rows: 3\n")
	f.write("   cols: 3\n")
	f.write("   dt: d\n")
	f.write("   data: [ {0[0]}, {0[1]}, {0[2]},\n          {0[4]}, {0[5]}, {0[6]},\n          {0[8]}, {0[9]}, {0[10]}]\n".
			format(cam1_imu_transformation))
	f.write("#Translation from camera frame to imu frame, imu^T_cam\n")
	f.write("extrinsicTranslation: !!opencv-matrix\n")
	f.write("   rows: 3\n")
	f.write("   cols: 1\n")
	f.write("   dt: d\n")
	f.write("   data: [ {0[3]}, {0[7]}, {0[11]}]\n".
			format(cam1_imu_transformation))
	f.write("\n")

	f.close()

	pass

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

def kalibr2slam(stereo_yaml,imucam_yaml,description=''):
	"""
	change Kalibr yaml to SLAM-OB yaml(YAML:1.0 for OpenCV)
	"""
	if len(description)>0 and description[0]!="#":
		description="#"+description

	stereo=open_yaml(stereo_yaml)
	imucam=open_yaml(imucam_yaml)

	cam0_internal=stereo["cam0"]["intrinsics"]
	cam0_distortion=stereo["cam0"]["distortion_coeffs"]
	imu_cam0_time=imucam["cam0"]["timeshift_cam_imu"]
	cam0_imu_transformation=numpy.array(numpy.linalg.inv(numpy.matrix(imucam["cam0"]["T_cam_imu"])))
	cam0_cam1_transformation=stereo["cam1"]["T_cn_cnm1"]

	write_cam0_yaml(cam0_internal,cam0_distortion,imu_cam0_time,cam0_imu_transformation,cam0_cam1_transformation,description)

	cam1_internal=stereo["cam1"]["intrinsics"]
	cam1_distortion=stereo["cam1"]["distortion_coeffs"]
	if str(imucam).find("cam1")>0 and str(imucam["cam1"]).find("timeshift_cam_imu")>0:
		imu_cam1_time=imucam["cam1"]["timeshift_cam_imu"]
	else:
		imu_cam1_time=imucam["cam0"]["timeshift_cam_imu"]

	if str(imucam).find("cam1")>0 and str(imucam["cam1"]).find("T_cam_imu")>0:
		cam1_imu_transformation=numpy.array(numpy.linalg.inv(numpy.matrix(imucam["cam1"]["T_cam_imu"])))
	else:
		cam1_cam0_Rt=numpy.linalg.inv(numpy.matrix(cam0_cam1_transformation))
		cam0_imu_Rt=numpy.matrix(cam0_imu_transformation)
		cam1_imu_transformation=numpy.array(cam0_imu_Rt*cam1_cam0_Rt)
	write_cam1_yaml(cam1_internal,cam1_distortion,imu_cam1_time,cam1_imu_transformation,description)


# file1="/media/hi/warehouse/G2-clb/slamdata-hte01/2/camchain-glasses2.yaml"
# file2="/media/hi/warehouse/G2-clb/slamdata-hte01/2/camchain-imucam-glasses2.yaml"

if __name__ == '__main__':
	if len(sys.argv)<3:
		print("Usage: python stereo_yaml imucam_yaml (description)")
		exit(1)
	import time
	import os
	description="#calibrate"
	description+= time.strftime("-%Y%m%d%H%M%S",time.localtime(os.stat(sys.argv[1]).st_mtime))
	if len(sys.argv)==4:
		description+="-"+sys.argv[3]

	kalibr2slam(sys.argv[1],sys.argv[2],description)
	print(description)
	print("Finish")