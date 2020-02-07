import time

import pyautogui
import pygame

import api
import settings

color = (131, 197, 226)

stops = [
    (1402, 1433, 1),
    (1439, 1290, 0),
    (1435, 1151, 0),
    (1377, 1064, 1)
]

def getLocation():
    img = pyautogui.screenshot()
    (width, height) = img.size
    f = False
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            if color == img.getpixel((x, y)):
                return ((x - (width - height) // 2) * 1500 // height, y * 1500 // height)

    return -1, -1


lastStop = (0, 0)

pygame.mixer.init()

while True:
    x, y = getLocation()
    print(x, y)
    name = 0
    for stop in stops:
        name += 1
        xi, yi = stop
        if abs(xi-x) <= 15 and abs(yi-y) <=15 and lastStop != stop:
            lastStop = stop
            pygame.mixer.music.load("data/audio/" + str(name) + ".mp3")
            pygame.mixer_music.set_volume(1)
            pygame.mixer.music.play(loops=0, start=0.0)
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    time.sleep(1.5)

