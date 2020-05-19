#!/usr/bin/python3
import json
import os


class Profile():
    def __init__(self):
        self.cmd_id = ""
        self.cmd_stereoimu_start = ""
        self.cmd_stereoimu_stop = ""
        self.cmd_fergb = ""
        self.cmd_fe = ""
        self.cmd_rgb = ""
        self.cmd_imu = ""
        self.cmd_pull_data = ""

        self.path_stereoimu = ""
        self.path_fe = ""
        self.path_rgb = ""
        self.path_imu = ""

    def load_profile(self, json_file):
        try:
            f = open(json_file, 'r')
        except:
            print("open failed", json_file)
            return False

        config = json.load(f)
        # 后续添加判断命令是否存在
        self.cmd_id = config["Command"]["ID_device"]
        self.cmd_stereoimu_start = config["Command"]["FE_IMU_capture_start"]
        self.cmd_stereoimu_stop = config["Command"]["FE_IMU_capture_stop"]
        self.cmd_fergb = config["Command"]["FE_RGB_capture"]
        self.cmd_rgb = config["Command"]["RGB_capture"]
        self.cmd_fe = config["Command"]["FE_capture"]
        self.cmd_imu = config["Command"]["IMU_capture_start"]
        self.cmd_pull_data=config["Command"]["Pull_data"]

        self.path_fe=config["DevicePath"]["FE_path"]
        self.path_rgb=config["DevicePath"]["RGB_path"]
        self.path_stereoimu=config["DevicePath"]["FE_IMU_path"]
        self.path_imu=config["DevicePath"]["IMU_path"]

    def send_command(self, command):
        print("sc", command)
        f = os.popen(command)
        output = f.read()
        f.close()
        return output

    def pull_data(self, src_path, dst_path):
        print("pd",self.cmd_pull_data+" "+src_path+" "+dst_path)
        os.system(self.cmd_pull_data+" "+src_path+" "+dst_path)
