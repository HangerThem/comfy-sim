import time
from pydualsense import *

dualsense = pydualsense()
dualsense.init()


while not dualsense.state.cross:
    dualsense.setLeftMotor(255)
    dualsense.setRightMotor(255)
    dualsense.light.setColorI(255, 0, 0)
    time.sleep(0.1)

    dualsense.setLeftMotor(0)
    dualsense.setRightMotor(0)
    dualsense.light.setColorI(0, 0, 0)
    time.sleep(0.5)


dualsense.setLeftMotor(0)
dualsense.setRightMotor(0)
time.sleep(0.5)
dualsense.close()
