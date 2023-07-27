import time
from pydualsense import *

ds = pydualsense()
ds.init()


while not ds.state.cross:
    ds.setLeftMotor(255)
    ds.setRightMotor(255)
    ds.light.setColorI(255, 0, 0)
    time.sleep(0.1)

    ds.setLeftMotor(0)
    ds.setRightMotor(0)
    ds.light.setColorI(0, 0, 0)
    time.sleep(0.5)


ds.setLeftMotor(0)
ds.setRightMotor(0)
time.sleep(0.5)
ds.close()
