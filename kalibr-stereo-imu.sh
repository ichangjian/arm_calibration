#!/bin/bash
kalibr_cde_path=$1
data_path=$2

export PATH=$kalibr_cde_path:$PATH
echo $data_path

time_begin=$(date +%s)

#create images and IMU data to ROS bag. 
#output 'basename.bag'
cde-exec kalibr_bagcreater --folder $data_path --output-bag stereo.bag --skip 7
cde-exec kalibr_bagcreater --folder $data_path --output-bag stereoimu.bag


#calibrate two cameras, intrinsic and extrinsic. 
#input 'basename.bag'
#output 'camchain-basename.yaml'
cde-exec kalibr_calibrate_cameras --target "$kalibr_cde_path/april_6x6.yaml" --bag stereo.bag \
--models pinhole-equi pinhole-equi --topics /cam0/image_raw /cam1/image_raw \
--dont-show-report --dont-generate-report 
#
cp camchain-stereo.yaml stereo.yaml
cat camchain-stereo.yaml |head -n 9 >stereo_cam0.yaml


#calibrate cameras and imu extrinsic. 
#input 'basename.bag', and output of last step: 'camchain-basename.yaml'
#output 'camchain-imucam-basename.yaml' and imu-glasses.yaml
cde-exec kalibr_calibrate_imu_camera --target "$kalibr_cde_path/april_6x6.yaml" --cam stereo_cam0.yaml  --imu "$kalibr_cde_path/imu_lenovo.yaml" --bag stereoimu.bag --dont-show-report  --dont-generate-report #--show-extraction 
#
cp camchain-imucam-stereoimu.yaml imu_cam0.yaml

time_end=$(date +%s)
echo "time spend $(($time_end -$time_begin))s"

rm stereo.bag
rm stereoimu.bag