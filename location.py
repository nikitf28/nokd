# -*- coding: utf-8 -*-
import keyboard as keyboard
import pyautogui
import time

import pygame

import api
from PyQt5.QtCore import QThread

import settings

color = (131, 197, 226)

stops = [
    (1056, 1413, 0, 'Макдональдс', '2.mp3', 0),
    (1110, 1352, 0, 'Водная школа', '3.mp3', 0),
    (1138, 1358, 0, 'ЦГБ', '4.mp3', 0),
    (1216, 1454, 0, 'Автостоянка', '5.mp3', 0),
    (1307, 1446, 0, 'Автосервис', '6.mp3', 0),
    (1404, 1443, 0, 'Вокзал', '7.mp3', 0),
    (1345, 1374, 0, 'Красный октябрь', '8.mp3', 0),
    (1400, 1244, 0, 'Автосалон', '9.mp3', 0),
    (1398, 1163, 0, 'Авктошкола(улица)', '10.mp3', 0),
    (1362, 1063, 1, 'ТТУ', '11.mp3', 0),
    (1393, 1147, 0, 'Автошкола(шоссе)', '10.mp3', 1),
    (1430, 1280, 0, 'Автосалон', '9.mp3', 1),
    (1404, 1443, 0, 'Вокзал', '7.mp3', 1),
    (1307, 1446, 0, 'Автосервис', '6.mp3', 1),
    (1216, 1454, 0, 'Автостоянка', '5.mp3', 1),
    (1155, 1358, 0, 'ЦГБ', '4.mp3', 1),
    (1098, 1358, 0, 'Водная школа', '3.mp3', 1),
    (962, 1445, 1, 'АТП', '1.mp3', 1),
]


def getLocation():
    img = pyautogui.screenshot()
    (width, height) = img.size
    f = False
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            if color == img.getpixel((x, y)):
                return (x - (width - height) // 2) * 1500 // height, y * 1500 // height

    return -1, -1


def playAudio(path):
    pyautogui.keyDown('/')
    # time.sleep(0.5)
    pygame.mixer.music.load(path)
    pygame.mixer_music.set_volume(1)
    pygame.mixer.music.play(loops=0, start=0.0)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
        time.sleep(1)
    pyautogui.keyUp('/')

def infoKey():
    playAudio('data/audio/priv.mp3')

lastStop = (0, 0)
way = 1
pygame.mixer.init()


class LocationControl(QThread):

    def __init__(self, mainWindow, openDoorKey, voiceKey, warnDoorKey, routeInfoKey, welcomeKey, parent=None):
        super(LocationControl, self).__init__(parent)
        #print('INIT')
        self.welcomeKey = welcomeKey
        self.routeInfoKey = routeInfoKey
        self.warnDoorKey = warnDoorKey
        self.voiceKey = voiceKey
        self.openDoorKey = openDoorKey
        self.mainWindow = mainWindow
        #print('Init Finished')
        self.initKeys(routeInfoKey)

    def initKeys(self, routeInfoKey):
        #if self.warnDoorKey != '':
        #    keyboard.add_hotkey('Ctrl+' + self.warnDoorKey, )
        if routeInfoKey != '':
            try:
                keyboard.add_hotkey('Ctrl+' + self.routeInfoKey, infoKey)
            except Exception as err:
                print(err)

        #if self.welcomeKey != '':
        #    keyboard.add_hotkey('Ctrl+' + self.welcomeKey, )

    def run(self):
        while True:
            if not settings.located_status:
                break
            x, y = getLocation()
            api.updateWork(settings.username, str(x), str(y - 40))

            num = 0
            for stop in stops:
                xi, yi, typ, name, file, w = stop
                if abs(xi - x) <= 15 and abs(yi - y) <= 15 and lastStop != stop and w == way:
                    pyautogui.keyDown('/')
                    if typ == 1:
                        # x1, y1, typ1, name1, file2, w1 = stops[num + 1]
                        playAudio('data/audio/' + str(file))
                        playAudio('data/audio/pok.mp3')
                        way = abs(1 - way)
                    if typ == 0:
                        # x1, y1, typ1, name1, file2, w1 = stops[num + 1]
                        playAudio('data/audio/' + file)
                        playAudio('data/audio/next.mp3')
                        print("NUM ", num)
                        x1, y1, typ1, name1, file1, w1 = stops[num + 1]
                        playAudio('data/audio/' + file1)
                    lastStop = stop
                    pyautogui.keyUp('/')

                num += 1

            time.sleep(5)
