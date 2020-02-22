# -*- coding: utf-8 -*-
import keyboard as keyboard
import pyautogui
import time

import api
from PyQt5.QtCore import QThread


import settings

color = (131, 197, 226)


def getLocation():
    img = pyautogui.screenshot()
    (width, height) = img.size
    f = False
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            if color == img.getpixel((x, y)):
                return (x - (width - height) // 2) * 1500 // height, y * 1500 // height

    return -1, -1


class LocationControl(QThread):

    def __init__(self, mainWindow, openDoorKey, voiceKey, warnDoorKey, routeInfoKey, welcomeKey,  parent=None):
        super(LocationControl, self).__init__(parent)
        self.welcomeKey = welcomeKey
        self.routeInfoKey = routeInfoKey
        self.warnDoorKey = warnDoorKey
        self.voiceKey = voiceKey
        self.openDoorKey = openDoorKey
        self.mainWindow = mainWindow

    def initKeys(self):
        if self.warnDoorKey != '':
            keyboard.add_hotkey('Ctrl+' + self.warnDoorKey, )
        if self.routeInfoKey !=  '':
            keyboard.add_hotkey('Ctrl+' + self.routeInfoKey, )
        if self.welcomeKey != '':
            keyboard.add_hotkey('Ctrl+' + self.welcomeKey, )

    def run(self):
        while True:
            if not settings.located_status:
                break
            x, y = getLocation()
            api.updateWork(settings.username, str(x), str(y - 40))
            time.sleep(10)
