import pygame
import time
from pydualsense import *

pygame.init()
ds = pydualsense()

screen = pygame.display.set_mode((360, 520))
pygame.display.set_caption("ComfySim client")

clock = pygame.time.Clock()

x, y = pygame.mouse.get_pos()
t = pygame.time.get_ticks()

speed = 0
speeds = [0] * 10

cursor_positions = []

colors = [[255, 20, 147], [238, 130, 238], [
    173, 216, 230], [255, 165, 0], [255, 0, 0]]

colorIndex = 0
color = colors[colorIndex]

connected = False

motorPercent = 50

running = True

modes = ["Joystick", "Spike", "Swipe"]
modeIndex = 0

spikesUp = False

errorTTL = 0


def dpad_right(state):
    if state == False:
        return
    global colorIndex, color
    colorIndex += 1
    if colorIndex >= len(colors):
        colorIndex = 0
    color = colors[colorIndex]
    ds.light.setColorI(color[0], color[1], color[2])


def dpad_left(state):
    if state == False:
        return
    global colorIndex, color
    colorIndex -= 1
    if colorIndex < 0:
        colorIndex = len(colors) - 1
    color = colors[colorIndex]
    ds.light.setColorI(color[0], color[1], color[2])


def up_motor(state):
    if state == False:
        return
    global motorPercent
    motorPercent -= 10
    if motorPercent < 0:
        motorPercent = 0


def down_motor(state):
    if state == False:
        return
    global motorPercent
    motorPercent += 10
    if motorPercent > 100:
        motorPercent = 100


def left_joystick_changed(x, y):
    speed = max(0, min((2 * (abs(x) + abs(y)) - 20), 255))
    speeds.append(speed)
    speeds.pop(0)


def closeDS():
    ds.setLeftMotor(0)
    ds.setRightMotor(0)
    ds.light.setColorI(0, 0, 0)
    time.sleep(0.1)
    ds.close()


def add_cursor_position(x, y):
    cursor_positions.append((x, y, pygame.time.get_ticks()))


def change_mode(state):
    if state == False:
        return
    global modeIndex
    modeIndex += 1
    if modeIndex >= len(modes):
        modeIndex = 0
    update_mode_id()
    if modeIndex == 0:
        ds.left_joystick_changed += left_joystick_changed
    elif modeIndex == 1:
        ds.left_joystick_changed -= left_joystick_changed


def update_mode_id():
    if modeIndex == 0:
        ds.light.setPlayerID(PlayerID.PLAYER_1)
    if modeIndex == 1:
        ds.light.setPlayerID(PlayerID.PLAYER_2)
    if modeIndex == 2:
        ds.light.setPlayerID(PlayerID.PLAYER_3)


def connect_controller():
    global connected, errorTTL
    try:
        ds.init()
        connected = True
    except:
        errorTTL = 60


ds.dpad_left += dpad_left
ds.dpad_right += dpad_right
ds.l1_changed += up_motor
ds.r1_changed += down_motor
ds.left_joystick_changed += left_joystick_changed
ds.circle_pressed += change_mode

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            if connected:
                closeDS()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                if connected:
                    closeDS()
                quit()
            if event.key == pygame.K_c:
                connect_controller()
            if connected:
                if event.key == pygame.K_LEFT:
                    dpad_left(True)
                if event.key == pygame.K_RIGHT:
                    dpad_right(True)
                if event.key == pygame.K_DOWN:
                    up_motor(True)
                if event.key == pygame.K_UP:
                    down_motor(True)
                if event.key == pygame.K_SPACE:
                    change_mode(True)

    screen.fill((color))

    if connected:
        cx, cy = pygame.mouse.get_pos()
        ct = pygame.time.get_ticks()

        dx, dy = cx - x, cy - y
        dt = ct - t

        if modes[modeIndex] == "Spike":
            if spikesUp:
                if speed < 255:
                    speed += 100
                else:
                    spikesUp = False
            else:
                if speed > 0:
                    speed -= 100
                else:
                    spikesUp = True
        elif modes[modeIndex] == "Swipe":
            speed = ((dx ** 2 + dy ** 2) ** 0.5) / dt * 175

        speed = max(0, min(speed, 255))
        speeds.pop(0)
        speeds.append(speed)
        speed = sum(speeds) / len(speeds)

        x, y = cx, cy
        t = ct

        add_cursor_position(cx, cy)

        ds.setLeftMotor(int(speed * motorPercent / 100))
        ds.setRightMotor(int(speed * motorPercent / 100))
        r = int(color[0] * speed / 255)
        g = int(color[1] * speed / 255)
        b = int(color[2] * speed / 255)
        ds.light.setColorI(r, g, b)

        for i in range(1, len(cursor_positions)):
            thickness = int(i*1.2)
            pygame.draw.line(screen, (255, 255, 255),
                             cursor_positions[i - 1][:2], cursor_positions[i][:2], thickness)
            pygame.draw.circle(screen, (255, 255, 255),
                               cursor_positions[i][:2], thickness // 2)
        font = pygame.font.SysFont("calibri", 20)

        text = font.render(
            "Motor: " + str(motorPercent) + "%" + " | " + "Intensity: " + str(int(speed)), 1, (0, 0, 0))
        screen.blit(text, (10, 30))

        text = font.render(
            "Mode: " + modes[modeIndex] + " | " + "Connected via: " + str(ds.conType).split(".")[1], 1, (0, 0, 0))
        screen.blit(text, (10, 10))

    else:
        font = pygame.font.SysFont("calibri", 25)
        text = font.render(
            "Press C to connect", 1, (0, 0, 0))
        screen.blit(text, (85, 230))

        if errorTTL > 0:
            font = pygame.font.SysFont("calibri", 15)

            text = font.render(
                "No contoller connected", 1, (0, 0, 0))
            screen.blit(text, (107.5, 255))
            errorTTL -= 1

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 360, 520), 5)

    pygame.display.update()

    clock.tick(60)

    while len(cursor_positions) > 25:
        cursor_positions.pop(0)
