#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QPushButton,
                             QTextBrowser, QVBoxLayout, QWidget)
import calib_device


class calibration(QWidget):

    def __init__(self, parent=None):
        super(calibration, self).__init__(parent)
        layout = QVBoxLayout()

        # with open('calib_profile.json', 'r') as f:
        #     config = json.load(f)
        # self.config = config
 
        self.label_state = QLabel()
        self.label_state.setText("状态显示")
        layout.addWidget(self.label_state)
        self.setWindowTitle("Calibration For newG2")

        self.content_log = QTextBrowser()
        layout.addWidget(self.content_log)

        self.label_version = QLabel()
        self.label_version.setText("工厂标定 版本1.2")
        layout.addWidget(self.label_version)

        self.btn_work_path = QPushButton()
        self.btn_work_path.clicked.connect(self.select_path)
        self.btn_work_path.setText("1.选定工作目录")
        layout.addWidget(self.btn_work_path)

        self.btn_device_calib = QPushButton()
        self.btn_device_calib.clicked.connect(self.device_calib_clk)
        self.btn_device_calib.setText("2.标定设备(FE+RGB+IMU)")
        layout.addWidget(self.btn_device_calib)

        self.btn_imu_calib = QPushButton()
        self.btn_imu_calib.clicked.connect(self.imu_calib_clk)
        self.btn_imu_calib.setText("3.IMU自身标定")
        layout.addWidget(self.btn_imu_calib)

        self.btn_file_check = QPushButton()
        self.btn_file_check.clicked.connect(self.file_check_clk)
        self.btn_file_check.setText("4.标定文件比对")
        layout.addWidget(self.btn_file_check)

        self.label_test = QLabel()
        self.label_test.setText("调试功能")
        layout.addWidget(self.label_test)

        self.btn_read_ID = QPushButton()
        self.btn_read_ID.clicked.connect(self.read_ID_clk)
        self.btn_read_ID.setText("Read Device ID")
        layout.addWidget(self.btn_read_ID)

        self.btn_capture_stereoimu_start = QPushButton()
        self.btn_capture_stereoimu_start.clicked.connect(self.capture_stereoimu_start_clk)
        self.btn_capture_stereoimu_start.setText("SLAM标定开始抓图")
        layout.addWidget(self.btn_capture_stereoimu_start)

        self.btn_capture_stereoimu_stop = QPushButton()
        self.btn_capture_stereoimu_stop.clicked.connect(self.capture_stereoimu_stop_clk)
        self.btn_capture_stereoimu_stop.setText("SLAM标定结束抓图")
        layout.addWidget(self.btn_capture_stereoimu_stop)

        self.btn_compute_stereoimu = QPushButton()
        self.btn_compute_stereoimu.clicked.connect(self.compute_stereoimu_clk)
        self.btn_compute_stereoimu.setText("计算SALM参数")
        layout.addWidget(self.btn_compute_stereoimu)

        self.btn_save_path = QPushButton()
        self.btn_save_path.clicked.connect(self.save_path_clk)
        self.btn_save_path.setText("选择保存路径")
        layout.addWidget(self.btn_save_path)
    
        self.btn_capture_fe = QPushButton()
        self.btn_capture_fe.clicked.connect(self.capture_fe_clk)
        self.btn_capture_fe.setText("FE抓图")
        layout.addWidget(self.btn_capture_fe)

        self.btn_capture_rgb = QPushButton()
        self.btn_capture_rgb.clicked.connect(self.capture_rgb_clk)
        self.btn_capture_rgb.setText("RGB抓图")
        layout.addWidget(self.btn_capture_rgb)

        self.setLayout(layout)
        self.device_ID = ' '
        self.save_path = ' '
        self.work_path = ' '
        self.__fun=calib_device
    def select_path(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "choose directory", "")
        self.work_path = dir_path
        self.content_log.append('当前选择目录为：'+self.work_path)

    def device_calib_clk(self):
        self.__fun.device_data_capture(self.content_log)

    def imu_calib_clk(self):
        pass

    def file_check_clk(self):
        pass

    def read_ID_clk(self):
        pass

    def capture_stereoimu_start_clk(self):
        pass

    def capture_stereoimu_stop_clk(self):
        pass

    def compute_stereoimu_clk(self):
        pass

    def save_path_clk(self):
        pass

    def capture_fe_clk(self):
        pass

    def capture_rgb_clk(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calib = calibration()
    calib.show()
    sys.exit(app.exec_())