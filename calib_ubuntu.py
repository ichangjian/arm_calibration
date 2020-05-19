#!/usr/bin/python3
import os
import time
import calib_robot
import calib_device
import yaml_format


class Ubuntu():
    def __init__(self, file_profile):
        self.device = calib_device.Device(file_profile)
        self.robot = calib_robot.Robot(self.device)

        self.work_path = ""
        self.save_rgb_dir = "fe-rgb/cam1"
        self.save_fe_dir = "fe-rgb/cam0"
        self.save_imu_dir = "imu"
        self.save_stereoimu_dir = "cam-imu"
        self.save_path = ""
        self.kalibr_path=self.device.profile.path_kalibr
        self.stereo_imu_sh="kalibr-stereo-imu.sh"
        self.feleft_rgb_sh="kalibr-fe-rgb.sh"
        self.sh_path=os.path.split(os.path.realpath(__file__))[0]

    def set_work_path(self, path):
        self.work_path = path

    def read_ID_clk(self,log=[]):
        self.device_id = self.device.get_device_ID(log)
        print(self.device_id)

    def compute_stereoimu(self, log=[]):
        log.append("计算stereoimu")
        os.chdir(self.save_path)
        os.system(os.path.join(self.sh_path,self.stereo_imu_sh)+" "+self.kalibr_path+" "+os.path.join(self.save_path, self.save_stereoimu_dir))

    def compute_fergb(self, log=[]):
        log.append("计算fergb")
        os.chdir(self.save_path)
        os.system(os.path.join(self.sh_path,self.feleft_rgb_sh)+" "+self.kalibr_path+" "+os.path.join(self.save_path, self.save_rgb_dir+"/.."))

    def compute_imu_state(self, log=[]):
        pass

    def compute_imu_bias(self, log=[]):
        pass

    def device_calib_clk(self, log=[]):
        self.capture_device_cv(log)
        self.compute_stereoimu(log)
        self.compute_fergb(log)

    def imu_calib_clk(self):
        pass

    def file_check_clk(self):
        pass

    def capture_device_cv(self, log=[]):

        self.read_ID_clk()
        log.append("设备ID:"+self.device_id)
        self.set_save_path(os.path.join(self.work_path, self.device_id))

        self.robot.move_arm_stereoimu(os.path.join(
            self.save_path, self.save_stereoimu_dir), log)
        self.robot.move_arm_fergb(os.path.join(self.save_path, self.save_fe_dir), os.path.join(
            self.save_path, self.save_rgb_dir), log)

    def capture_stereoimu_start_clk(self):
        if self.save_path == "":
            print("please select work space")
            return False

        self.device.capture_command_stereoimu_start()

    def capture_stereoimu_stop_clk(self):
        self.device.capture_command_stereoimu_stop()
        time.sleep(0.5)
        self.device.pull_stereoimu_data(self.save_path)

    def set_save_path(self, path):
        if not os.path.exists(path):
            pass #os.system("rm -r "+path)

        # os.mkdir(path)
        self.save_path = path

    def capture_fe_clk(self, file_fe_name):
        if self.save_path == "":
            print("please select work space")
            return False

        if not self.device.capture_command_fe():
            print("capture failed")
            return False

        save_fe_path = self.save_path #os.path.join(self.save_path, self.save_fe_dir)
        if not os.path.exists(save_fe_path):
            os.makedirs(save_fe_path)

        time.sleep(0.5)
        self.device.pull_fe_data(os.path.join(save_fe_path, file_fe_name))

    def capture_rgb_clk(self, file_rgb_name):
        if not self.device.capture_command_rgb():
            print("capture failed")
            return False

        if self.save_path == "":
            print("please select work space")
            return False

        save_rgb_path = self.save_path#os.path.join(self.save_path, self.save_rgb_dir)
        if not os.path.exists(save_rgb_path):
            os.makedirs(save_rgb_path)
        time.sleep(0.5)
        self.device.pull_rgb_data(os.path.join(save_rgb_path, file_rgb_name))

    def capture_fergb_clk(self, file_fergb_name):
        if self.save_path == "":
            print("please select work space")
            return False

        if not self.device.capture_command_fergb():
            print("capture failed")
            return False

        save_fe_path = os.path.join(self.save_path, self.save_fe_dir)
        if not os.path.exists(save_fe_path):
            os.makedirs(save_fe_path)

        self.device.pull_fe_data(os.path.join(save_fe_path, file_fergb_name))
        save_rgb_path = os.path.join(self.save_path, self.save_rgb_dir)
        if not os.path.exists(save_rgb_path):
            os.makedirs(save_rgb_path)

        self.device.pull_rgb_data(os.path.join(save_rgb_path, file_fergb_name))
