from pydualsense import *
import math as Math

intensity = 0


def set_intensity():
    global intensity
    dualsense.setLeftMotor(intensity)
    dualsense.setRightMotor(intensity)


def update_color():
    global intensity
    dualsense.light.setColorI(intensity, intensity, intensity)


def up_intensity(state):
    global intensity
    if intensity > 254:
        intensity = 255
    else:
        intensity += 1
    dualsense.audio.microphone_led = True
    set_intensity()
    update_color()


def down_intensity(state):
    global intensity
    if intensity < 1:
        intensity = 0
    else:
        intensity -= 1
    dualsense.audio.microphone_led = False
    set_intensity()
    update_color()


def max_intensity(state):
    global intensity
    intensity = 255
    set_intensity()
    update_color()


def min_intensity(state):
    global intensity
    intensity = 0
    set_intensity()
    update_color()


# create dualsense
dualsense = pydualsense()
# find device and initialize
dualsense.init()

# add events handler functions
dualsense.dpad_down += down_intensity
dualsense.dpad_up += up_intensity
dualsense.dpad_left += min_intensity
dualsense.dpad_right += max_intensity

# read controller state until R1 is pressed
while not dualsense.state.cross:
    ...

# close device
dualsense.close()
