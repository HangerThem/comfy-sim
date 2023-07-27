import time
from pydualsense import *

dualsense = pydualsense()
dualsense.init()

colors = [[255, 20, 147], [238, 130, 238], [
    173, 216, 230], [255, 165, 0], [255, 0, 0]]
colorIndex = 0
color = colors[colorIndex]

leftMotorPercent = .5
rightMotorPercent = .5


def left_joystick_changed(x, y):

    speed = 2 * (abs(x) + abs(y)) - 15

    intensity = max(0, min(speed, 255))

    dualsense.setLeftMotor(int(intensity * leftMotorPercent))
    dualsense.setRightMotor(int(intensity * rightMotorPercent))

    r = int(color[0] * intensity/255)
    g = int(color[1] * intensity/255)
    b = int(color[2] * intensity/255)
    dualsense.light.setColorI(r, g, b)

    time.sleep(0.01)


def dpad_right(state):
    if state == False:
        return
    global colorIndex, color
    colorIndex += 1
    if colorIndex >= len(colors):
        colorIndex = 0
    color = colors[colorIndex]
    dualsense.light.setColorI(color[0], color[1], color[2])


def dpad_left(state):
    if state == False:
        return
    global colorIndex, color
    colorIndex -= 1
    if colorIndex < 0:
        colorIndex = len(colors) - 1
    color = colors[colorIndex]
    dualsense.light.setColorI(color[0], color[1], color[2])


def up_left_motor(state):
    if state == False:
        return
    global leftMotorPercent
    leftMotorPercent += .1
    if leftMotorPercent > 1:
        leftMotorPercent = 1


def down_left_motor(state):
    if state == False:
        return
    global leftMotorPercent
    leftMotorPercent -= .1
    if leftMotorPercent < 0:
        leftMotorPercent = 0


def up_right_motor(state):
    if state == False:
        return
    global rightMotorPercent
    rightMotorPercent += .1
    if rightMotorPercent > 1:
        rightMotorPercent = 1


def down_right_motor(state):
    if state == False:
        return
    global rightMotorPercent
    rightMotorPercent -= .1
    if rightMotorPercent < 0:
        rightMotorPercent = 0


dualsense.left_joystick_changed += left_joystick_changed
dualsense.dpad_left += dpad_left
dualsense.dpad_right += dpad_right
dualsense.l1_changed += up_left_motor
dualsense.l2_changed += down_left_motor
dualsense.r1_changed += up_right_motor
dualsense.r2_changed += down_right_motor

while not dualsense.state.cross:
    ...

dualsense.setLeftMotor(0)
dualsense.setRightMotor(0)
time.sleep(0.5)
dualsense.close()
