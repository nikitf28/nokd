# -*- coding: utf-8 -*-


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

    def __init__(self, mainWindow, parent=None):
        super(LocationControl, self).__init__(parent)
        self.mainWindow = mainWindow

    def run(self):
        while True:
            if not settings.located_status:
                break
            x, y = getLocation()
            api.updateWork(settings.username, str(x), str(y - 40))
            time.sleep(10)
