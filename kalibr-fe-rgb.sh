#!/bin/bash
kalibr_cde_path=$1
data_path=$2

export PATH=$kalibr_cde_path:$PATH
echo $data_path

time_begin=$(date +%s)

#create images and IMU data to ROS bag. 
#output 'basename.bag'
cde-exec kalibr_bagcreater --folder $data_path --output-bag feleft-rgb.bag


#calibrate two cameras, intrinsic and extrinsic. 
#input 'basename.bag'
#output 'camchain-basename.yaml'
cde-exec kalibr_calibrate_cameras --target "$kalibr_cde_path/april_6x6.yaml" --bag feleft-rgb.bag \
--models pinhole-equi pinhole-radtan --topics /cam0/image_raw /cam1/image_raw \
--dont-show-report --dont-generate-report
#
mv camchain-feleft-rgb.yaml rgb_fe.yaml

time_end=$(date +%s)
echo "time spend $(($time_end -$time_begin))s"

rm feleft-rgb.bag