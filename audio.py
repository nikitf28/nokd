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

def playAudio(path):
    pyautogui.keyDown('/')
    #time.sleep(0.5)
    pygame.mixer.music.load(path)
    pygame.mixer_music.set_volume(1)
    pygame.mixer.music.play(loops=0, start=0.0)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    time.sleep(0.5)
    pyautogui.keyUp('/')


lastStop = (0, 0)
way = 1
pygame.mixer.init()

while True:
    x, y = getLocation()
    print(x, y)
    name = 0
    for stop in stops:
        name += 1
        xi, yi, typ = stop
        if abs(xi-x) <= 15 and abs(yi-y) <=15 and lastStop != stop:
            pyautogui.keyDown('/')
            if typ == 1:
                playAudio('data/audio/' + str(name) + '.mp3')
                playAudio('data/audio/pok.mp3')
                way = abs(1 - way)
            if typ == 0:
                if way == 0:
                    playAudio('data/audio/' + str(name) + '.mp3')
                    playAudio('data/audio/next.mp3')
                    playAudio('data/audio/' + str(name+1) + '.mp3')
                if way == 1:
                    playAudio('data/audio/' + str(name) + '.mp3')
                    playAudio('data/audio/next.mp3')
                    playAudio('data/audio/' + str(name - 1) + '.mp3')
            lastStop = stop
            pyautogui.keyUp('/')


    time.sleep(1.5)

