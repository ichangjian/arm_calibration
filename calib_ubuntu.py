#!/usr/bin/python3

import calib_robot
import calib_device

class Ubuntu():
    def __init__(self,file_profile):
        self.device=calib_device.Device(file_profile)
        self.robot=calib_robot.Robot(self.device)

    def compute_stereoimu(self):
        pass

    def compute_fergb(self):
        pass

    def compute_imu_state(self):
        pass

    def compute_imu_bias(self):
        pass

    def compute_stereoimu(self):
        pass

    def device_calib_clk(self):
        self.__fun.device_data_capture(self.content_log)

    def imu_calib_clk(self):
        self.robot.im

    def file_check_clk(self):
        pass

    def read_ID_clk(self):
        return self.device.get_device_ID()

    def capture_stereoimu_start_clk(self):
        self.device.capture_command_stereoimu_start()

    def capture_stereoimu_stop_clk(self):
        self.device.capture_command_stereoimu_stop()

    def compute_stereoimu_clk(self):
        self.device.compute_stereoimu()

    def save_path_clk(self):
        pass

    def capture_fe_clk(self):
        self.device.capture_command_fe()

    def capture_rgb_clk(self):
        self.device.capture_command_rgb()


