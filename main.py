from pydualsense import *

ds = pydualsense()
ds.init()

print("Press the circle button to cycle through the modes.")

modes = ["joystick", "gyro", "spike"]

modeIndex = -1


def cycle_modes(state):
    global modeIndex
    if state == False:
        return
    modeIndex += 1
    if modeIndex >= len(modes):
        modeIndex = 0
    print(f"Mode: {modes[modeIndex]}")
    set_mode(modes[modeIndex])


def set_mode(mode):
    if mode == "spike":
        import spikeMode
    elif mode == "gyro":
        import gyroMode
    elif mode == "joystick":
        import joystickMode
    else:
        raise Exception("Invalid mode")


ds.circle_pressed += cycle_modes

while not ds.state.cross:
    ...

ds.close()
