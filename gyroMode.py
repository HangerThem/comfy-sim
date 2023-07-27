import time
from pydualsense import *


class DualSenseController:
    def __init__(self):
        self.ds = pydualsense()
        self.ds.init()
        self.gx, self.gy, self.gz = 0, 0, 0
        self.cx, self.cy, self.cz = 0, 0, 0
        self.ds.light.setColorI(255, 20, 147)
        self.ds.gyro_changed += self.gyro_changed
        self.ds.circle_pressed += self.close

    def gyro_changed(self, pitch, yaw, roll):
        self.gx, self.gy, self.gz = pitch, yaw, roll

        speed = abs((abs(self.cx - self.gx) + abs(self.cy -
                    self.gy) + abs(self.cz - self.gz)) - 9000)

        intensity = int(speed * 255 / 5500)

        intensity = max(0, min(intensity, 255))

        self.ds.setLeftMotor(intensity)
        self.ds.setRightMotor(intensity)
        self.ds.light.setColorI(intensity, 0, 0)

        self.cx, self.cy, self.cz = self.gx, self.gy, self.gz

        time.sleep(0.1)

    def close(self):
        self.ds.gyro_changed -= self.gyro_changed
        self.ds.setLeftMotor(0)
        self.ds.setRightMotor(0)
        time.sleep(0.5)
        self.ds.close()


DualSenseController()
