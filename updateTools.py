import os
from urllib.error import HTTPError

import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import settings
import api

iconPath = settings.iconPath

def updateProg():

    if os.path.exists('OLD.exe'):
        os.remove('OLD.exe')

    if api.countStat():
        settings.domain = 'https://nokd.ru'
        settings.pwd = '&pass=0a773ea7cb61f3d1655d731ff6507dc47b5481f4'



    serverVer = float(api.getVersion())
    if serverVer > settings.ver:
        succesBox = QMessageBox()
        succesBox.setIcon(QMessageBox.Information)
        succesBox.setText("Вышла новая версия клиента. Ожидайте завершение обновления. \n"
                          "Нажмите ОК для продолжения.")
        succesBox.setWindowTitle("Обновление")
        succesBox.setStandardButtons(QMessageBox.Ok)
        succesBox.setWindowIcon(QIcon(iconPath))
        succesBox.exec()

        print("You client is old! Update it!")
        if os.path.exists('Нокд - лаунчер.exe'):
            os.rename('Нокд - лаунчер.exe', 'OLD.exe')

        f = open(r'Нокд - лаунчер.exe', "wb")
        url = settings.domain + '/NOKD-bus.exe'
        ufr = requests.get(url)
        f.write(ufr.content)
        f.close()
        os.startfile(r'Нокд - лаунчер.exe')
        raise SystemExit(1)