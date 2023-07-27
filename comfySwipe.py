import pygame
import random
from pydualsense import *

pygame.init()
ds = pydualsense()
ds.init()

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

colorNames = ["DeepPink", "Violet", "LightBlue", "Orange", "Red"]

colorIndex = 0
color = colors[colorIndex]

motorPercent = 50


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


ds.dpad_left += dpad_left
ds.dpad_right += dpad_right
ds.l1_changed += up_motor
ds.r1_changed += down_motor


def add_cursor_position(x, y):
    cursor_positions.append((x, y, pygame.time.get_ticks()))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ds.close()
            quit()

    cx, cy = pygame.mouse.get_pos()
    ct = pygame.time.get_ticks()

    dx, dy = cx - x, cy - y
    dt = ct - t

    speed = ((dx ** 2 + dy ** 2) ** 0.5) / dt * 150

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
    screen.fill((255, 20, 147))

    font = pygame.font.SysFont("monospace", 15)

    text = font.render("Color: " + colorNames[colorIndex], 1, (255, 255, 255))
    screen.blit(text, (10, 10))

    text = font.render(
        "Motor: " + str(motorPercent) + "%", 1, (255, 255, 255))
    screen.blit(text, (10, 30))

    for i in range(1, len(cursor_positions)):
        thickness = int(i*1.2)
        pygame.draw.line(screen, (255, 255, 255),
                         cursor_positions[i - 1][:2], cursor_positions[i][:2], thickness)
        pygame.draw.circle(screen, (255, 255, 255),
                           cursor_positions[i][:2], thickness // 2)

    pygame.display.update()

    clock.tick(60)

    while len(cursor_positions) > 25:
        cursor_positions.pop(0)
