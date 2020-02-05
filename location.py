# -*- coding: utf-8 -*-


import pyautogui
import time

import api
from PyQt5.QtCore import QThread


import settings

color = (131, 197, 226)


class LocationControl(QThread):

    def __init__(self, mainWindow, parent=None):
        super(LocationControl, self).__init__(parent)
        self.mainWindow = mainWindow

    def run(self):
        while True:
            if not settings.located_status:
                #print('Finished!')
                break
            img = pyautogui.screenshot()
            (width, height) = img.size
            f = False
            for x in range(0, width, 1):
                for y in range(0, height, 1):
                    if color == img.getpixel((x, y)):
                        #self.mainWindow.logsBox.appendPlainText(str(x / width * 1000) + ' ' + str(y / height * 1000))
                        api.updateWork(settings.username, str((x - (width - height)//2)*1500//height ), str(y * 1450   // height - 40))
                        #print('X: ', x, 'width ', width, 'height ', height, 'full ', (x + (width - height)//2)*1500//width)
                        #print(str((x -   (width - height)//2)*1500//height), str(y * 1450 // height - 40))
                        #print(x*1500/width)
                        f = True
                        break
                        # return (x/width*1000, y/height*1000)
                if f:
                    break
            # return (-1, -1)
            #self.mainWindow.logsBox.appendPlainText('nothing')
            print('nothing')
            # QtCore.QThread.sleep(5)
            time.sleep(10)
