import time
from pydualsense import *

dualsense = pydualsense()
dualsense.init()

gx, gy, gz = 0, 0, 0
cx, cy, cz = 0, 0, 0


def gyro_changed(pitch, yaw, roll):
    global gx, gy, gz
    gx, gy, gz = pitch, yaw, roll

    speed = abs((abs(cx - gx) + abs(cy - gy) + abs(cz - gz)) - 9000)

    intensity = int(speed * 255 / 5500)

    intensity = max(0, min(intensity, 255))

    dualsense.setLeftMotor(intensity)
    dualsense.setRightMotor(intensity)
    dualsense.light.setColorI(intensity, 0, 0)

    print(f"intensity: {intensity}")
    print(f"speed: {speed}")

    gx, gy, gz = cx, cy, cz

    time.sleep(0.1)


dualsense.light.setColorI(255, 20, 147)


dualsense.gyro_changed += gyro_changed

while not dualsense.state.cross:
    ...

dualsense.gyro_changed -= gyro_changed
dualsense.setLeftMotor(0)
dualsense.setRightMotor(0)
time.sleep(0.5)
dualsense.close()
