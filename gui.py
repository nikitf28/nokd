# -*- coding: utf-8 -*-
import datetime
import json
import shutil
import sys
import os
import time

import api
import settings
import location
from configparser import ConfigParser, NoOptionError

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QPushButton, QComboBox, QFileDialog, \
    QMessageBox, QPlainTextEdit, QRadioButton, QCheckBox

import updateTools

gameDir = ''
iconPath = settings.iconPath
radarsetPath = '/MTA/MTA/cgui/images/radarset'
defaultFont = QFont('Arial', 10)
configFile = 'data/settings.conf'
parser = ConfigParser()
username = '-1'
buses = None
routes = None
color = (131, 197, 226)
timeBegin = 0


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        updateTools.updateProg()
        parser.read(configFile)
        initParser()
        global gameDir
        gameDir = parser.get('NOKD', 'game_path')
        self.logsBox = QPlainTextEdit()
        self.initUI()
        if username != '-1':
            initAutoInfo()

    def closeEvent(self, event):
        api.endWork(username, str((time.process_time() - timeBegin) // 60))

    def initUI(self):
        global loginEdit, passwordEdit, loginStatusText, driverNameText, driverOrganizationText, workButton, \
            breakButton, accidentButton, routeBox, busBox, graphicEdit, radiobutton1, radiobutton2, welcomeCheck, \
        routeCheck, stuffCheck, useInfoCheck, openDoorEdit, voiceEdit, warnDoorEdit, routeInfoEdit, welcomeEdit

        loginText = QLabel('Логин:', self)
        loginText.setFont(defaultFont)
        loginText.move(15, 10)

        loginEdit = QLineEdit(self)
        loginEdit.setGeometry(QRect(15, 30, 150, 25))
        loginEdit.setFont(defaultFont)
        loginEdit.setText(parser.get('NOKD', 'login'))

        passwordText = QLabel('Пароль:', self)
        passwordText.setFont(defaultFont)
        passwordText.move(15, 60)

        passwordEdit = QLineEdit(self)
        passwordEdit.setGeometry(QRect(15, 80, 150, 25))
        passwordEdit.setFont(defaultFont)
        passwordEdit.setEchoMode(QLineEdit.Password)
        passwordEdit.setText(parser.get('NOKD', 'password'))

        loginButton = QPushButton('Войти', self)
        loginButton.move(15, 110)
        loginButton.setFont(defaultFont)
        loginButton.clicked.connect(loginAPI)

        loginStatusText = QLabel(self)
        loginStatusText.move(15, 140)
        loginStatusText.setText('Вы не авторизированы')
        loginStatusText.setStyleSheet('color: rgb(204, 204, 0);')

        changeButton = QPushButton('Заменить файлы', self)
        changeButton.move(15, 160)
        changeButton.setFont(defaultFont)
        changeButton.clicked.connect(radarsetMode)

        returnButton = QPushButton('Вернуть файлы', self)
        returnButton.move(15, 190)
        returnButton.setFont(defaultFont)
        returnButton.clicked.connect(radarsetOriginal)

        pathButton = QPushButton('Путь к игре', self)
        pathButton.setFont(defaultFont)
        pathButton.move(15, 220)
        pathButton.clicked.connect(getfile)

        driverNameText = QLabel('Водитель:                                                                     ', self)
        driverNameText.move(230, 10)
        driverNameText.setFont(defaultFont)

        driverOrganizationText = QLabel('Организация:                                                          ', self)
        driverOrganizationText.move(230, 40)
        driverOrganizationText.setFont(defaultFont)

        busText = QLabel('Автобус: ', self)
        busText.move(230, 70)
        busText.setFont(defaultFont)

        busBox = QComboBox(self)
        busBox.setFont(defaultFont)
        busBox.setGeometry(QRect(290, 70, 250, 20))

        busText = QLabel('Маршрут: ', self)
        busText.move(230, 100)
        busText.setFont(defaultFont)
        busBox.setDisabled(True)

        routeBox = QComboBox(self)
        routeBox.setFont(defaultFont)
        routeBox.setGeometry(QRect(300, 100, 60, 20))
        routeBox.activated.connect(initAutoInfo)
        routeBox.setDisabled(True)

        workButton = QPushButton('  Выйти на линию   ', self)
        workButton.move(230, 130)
        workButton.setFont(defaultFont)
        workButton.setDisabled(True)
        workButton.clicked.connect(self.startWork)

        breakButton = QPushButton('Перерыв', self)
        breakButton.move(360, 130)
        breakButton.setFont(defaultFont)
        breakButton.setDisabled(True)

        accidentButton = QPushButton('ДТП', self)
        accidentButton.move(440, 130)
        accidentButton.setFont(defaultFont)
        accidentButton.setDisabled(True)

        graphicText = QLabel('График:', self)
        graphicText.setFont(defaultFont)
        graphicText.move(380, 100)

        graphicEdit = QLineEdit(self)
        graphicEdit.setGeometry(QRect(430, 100, 60, 20))
        graphicEdit.setFont(defaultFont)
        graphicEdit.setText('--')
        graphicEdit.setDisabled(True)

        radiobutton1 = QRadioButton("от A+1 до B                                                                ", self)
        radiobutton1.setFont(defaultFont)
        radiobutton1.setChecked(True)
        radiobutton1.route = 1
        radiobutton1.move(230, 200)

        radiobutton2 = QRadioButton("от B+1 до A                                                                ", self)
        radiobutton2.setFont(defaultFont)
        radiobutton2.route = 2
        radiobutton2.move(230, 220)

        openDoorText = QLabel('Открытие дверей:', self)
        openDoorText.setFont(defaultFont)
        openDoorText.move(230, 250)

        openDoorEdit = QLineEdit(self)
        openDoorEdit.setGeometry(QRect(340, 250, 15, 20))
        openDoorEdit.setFont(defaultFont)
        openDoorEdit.setText(parser.get('NOKD', 'openDoor'))

        voiceText = QLabel('Voice chat:', self)
        voiceText.setFont(defaultFont)
        voiceText.move(370, 250)

        voiceEdit = QLineEdit(self)
        voiceEdit.setGeometry(QRect(440, 250, 15, 20))
        voiceEdit.setFont(defaultFont)
        voiceEdit.setText(parser.get('NOKD', 'voice'))

        warnDoorText = QLabel('Предупреждение о закрытии: Ctrl+', self)
        warnDoorText.setFont(defaultFont)
        warnDoorText.move(230, 275)

        warnDoorEdit = QLineEdit(self)
        warnDoorEdit.setMaxLength(1)
        warnDoorEdit.setGeometry(QRect(440, 275, 15, 20))
        warnDoorEdit.setFont(defaultFont)
        warnDoorEdit.setText(parser.get('NOKD', 'warnDoor'))

        routeInfoText = QLabel('Информация о маршруте: Ctrl+', self)
        routeInfoText.setFont(defaultFont)
        routeInfoText.move(230, 300)

        routeInfoEdit = QLineEdit(self)
        routeInfoEdit.setMaxLength(1)
        routeInfoEdit.setGeometry(QRect(420, 300, 15, 20))
        routeInfoEdit.setFont(defaultFont)
        routeInfoEdit.setText(parser.get('NOKD', 'routeInfo'))

        welcomeText = QLabel('Приветствие: Ctrl+', self)
        welcomeText.setFont(defaultFont)
        welcomeText.move(230, 325)

        welcomeEdit = QLineEdit(self)
        welcomeEdit.setMaxLength(1)
        welcomeEdit.setGeometry(QRect(345, 325, 15, 20))
        welcomeEdit.setFont(defaultFont)
        welcomeEdit.setText(parser.get('NOKD', 'welcome'))

        welcomeCheck = QCheckBox('Приветствие', self)
        welcomeCheck.setFont(defaultFont)
        welcomeCheck.move(230, 180)     
        if parser.get('NOKD', 'welcomeCheck') == 'True':
            welcomeCheck.setChecked()

        routeCheck = QCheckBox('Маршрут', self)
        routeCheck.setFont(defaultFont)
        routeCheck.move(330, 180)
        if parser.get('NOKD', 'routeCheck') == 'True':
            routeCheck.setChecked()

        stuffCheck = QCheckBox('"Не забывайте свои вещи"', self)
        stuffCheck.setFont(defaultFont)
        stuffCheck.move(410, 180)
        if parser.get('NOKD', 'stuffCheck') == 'True':
            stuffCheck.setChecked()

        useInfoCheck = QCheckBox('Использовать автоинформатор', self)
        useInfoCheck.setFont(defaultFont)
        useInfoCheck.move(230, 160)
        if parser.get('NOKD', 'useInfoCheck') == 'True':
            useInfoCheck.setChecked()

        self.setWindowTitle('НОКД - клиент для водителей ЧАТП (' + settings.verString + ')')
        self.setWindowIcon(QIcon(iconPath))
        self.setFixedSize(600, 370)
        self.show()

        loginAPI()

    def startWork(self):
        if not settings.located_status:
            global timeBegin
            settings.located_status = True
            # accidentButton.setEnabled(True)
            # breakButton.setEnabled(True)
            busBox.setEnabled(False)
            routeBox.setEnabled(False)
            graphicEdit.setEnabled(False)
            workButton.setText('Закончить смену')
            timeBegin = datetime.datetime.now()
            api.startWork(username, routeBox.currentText(), graphicEdit.text())
            thread = location.LocationControl(parent=self, mainWindow=self, openDoorKey=openDoorEdit.text(),
                                              voiceKey=voiceEdit.text(), warnDoorKey=warnDoorEdit.text(),
                                              routeInfoKey=routeInfoEdit.text(), welcomeKey=welcomeEdit.text())
            thread.start()

        else:
            settings.located_status = False
            accidentButton.setEnabled(False)
            breakButton.setEnabled(False)
            graphicEdit.setEnabled(True)
            busBox.setEnabled(True)
            routeBox.setEnabled(True)
            workButton.setText('  Выйти на линию   ')
            api.endWork(username, str((datetime.datetime.now() - timeBegin) // 60))


def getfile():
    global gameDir
    dirName = QFileDialog.getExistingDirectory(None, "Укажить папку с Провинцией", gameDir)
    # print('b'+dirName+'e')
    # print(len(dirName))
    if os.path.exists(dirName + radarsetPath):
        gameDir = dirName
        cf = open(configFile, "w")
        parser.set('NOKD', 'game_path', gameDir)
        parser.write(cf)
    elif dirName != '':
        pathErrorBox = QMessageBox()
        pathErrorBox.setIcon(QMessageBox.Critical)
        pathErrorBox.setText(
            "Ничего нового. Ты так и не смог найти нужную папку. Повторяю: в этой папке фарминции нет!")
        pathErrorBox.setWindowTitle("Тупой водитель!")
        pathErrorBox.setStandardButtons(QMessageBox.Ok)
        pathErrorBox.setWindowIcon(QIcon(iconPath))
        pathErrorBox.exec()


def radarsetMode():
    copyFile('radarset_mode')


def radarsetOriginal():
    copyFile('radarset_original')


def copyFile(path):
    if os.path.exists(gameDir + radarsetPath):
        for num in range(1, 10):
            file1 = 'data/' + path + '/0' + str(num) + '.png'
            file2 = gameDir + radarsetPath + '/0' + str(num) + '.png'
            if os.path.exists(file1):
                shutil.copyfile(file1, file2)
            else:
                pass
                # print("ERROR!")
                # print(file1)

        for num in range(10, 64):
            file1 = 'data/' + path + '/' + str(num) + '.png'
            file2 = gameDir + radarsetPath + '/' + str(num) + '.png'
            if os.path.exists(file1):
                shutil.copyfile(file1, file2)

        file1 = 'data/' + path + '/up.png'
        file2 = gameDir + radarsetPath + '/up.png'
        if os.path.exists(file1):
            shutil.copyfile(file1, file2)

        file1 = 'data/' + path + '/down.png'
        file2 = gameDir + radarsetPath + '/down.png'
        if os.path.exists(file1):
            shutil.copyfile(file1, file2)

        file1 = 'data/' + path + '/square.png'
        file2 = gameDir + radarsetPath + '/square.png'
        if os.path.exists(file1):
            shutil.copyfile(file1, file2)
    else:
        pass
        # print('ERRO')
    succesBox = QMessageBox()
    succesBox.setIcon(QMessageBox.Information)
    succesBox.setText("Готово!")
    succesBox.setWindowTitle("Готово!")
    succesBox.setStandardButtons(QMessageBox.Ok)
    succesBox.setWindowIcon(QIcon(iconPath))
    succesBox.exec()


def loginAPI():
    global username, buses
    loginData = loginEdit.text()
    passwordData = passwordEdit.text()
    if loginData == '' or passwordData == '':
        return
    data = json.loads(api.login(loginData, passwordData))

    if data['ERROR_MODE'] == 1 and data['error'] == 'Password or username is not aviable':
        loginStatusText.setText('Неверный пароль!')
        loginStatusText.setStyleSheet('color: rgb(226, 0, 0);')
        global urername
        settings.username = ''
        username = ''
        driverNameText.setText('Водитель: ')
        driverOrganizationText.setText('Организация: ')
        workButton.setDisabled(True)
        breakButton.setDisabled(True)
        accidentButton.setDisabled(True)
        busBox.setEnabled(False)
        routeBox.setEnabled(False)
        graphicEdit.setDisabled(True)

    elif data['ERROR_MODE'] == 1:
        loginStatusText.setText('Ошибка входа!')
        loginStatusText.setStyleSheet('color: rgb(226, 0, 0);')
        global urername
        username = ''
        settings.username = ''
        driverNameText.setText('Водитель: ')
        driverOrganizationText.setText('Организация: ')
        workButton.setDisabled(True)
        breakButton.setDisabled(True)
        accidentButton.setDisabled(True)
        busBox.setEnabled(False)
        routeBox.setEnabled(False)
        graphicEdit.setDisabled(True)

    elif data['ERROR_MODE'] == 0 and data['data'] == 'OK':
        loginStatusText.setText('Успешно!')
        loginStatusText.setStyleSheet('color: rgb(30, 226, 0);')

        cf = open(configFile, "w")
        parser.set('NOKD', 'login', loginData)
        parser.set('NOKD', 'password', passwordData)
        parser.write(cf)

        nickName = api.html_decode(api.userNickname(loginData))
        # print(nickName)
        server = api.html_decode(api.userServer(loginData))
        organisationID = api.html_decode(api.userOrganisation(loginData))
        organisation = api.html_decode(api.getOrgName(organisationID))

        driverNameText.setText('Водитель: ' + nickName + ' #' + server)
        driverOrganizationText.setText('Организация: ' + organisation + ' [' + organisationID + ']')

        username = loginData

        settings.username = username

        workButton.setEnabled(True)
        busBox.setEnabled(True)
        routeBox.setEnabled(True)
        graphicEdit.setEnabled(True)
        # breakButton.setEnabled(True)
        # accidentButton.setEnabled(True)

        busBox.clear()
        buses = json.loads(api.getBuses(loginData))

        routes = json.loads(api.getRoutes(loginData))

        if buses is not None:
            busBox.addItem(api.html_decode(buses['model'] + ' ' + buses['number']))

        routeBox.clear()

        if routes is not None:
            for route in routes:
                routeBox.addItem(api.html_decode(route['number']))

        initAutoInfo()


def initAutoInfo():
    currentRoute = routeBox.currentText()
    nonParsedStops = api.getStops(currentRoute)
    if nonParsedStops is None:
        radiobutton1.setText('На данном маршруте нет автоинформатора')
        radiobutton2.setText('На данном маршруте нет автоинформатора')
        return
    busStops = json.loads(nonParsedStops)

    endStops = []

    #print(busStops)

    for i in range(len(busStops)):
        # print(busStops[i])
        if busStops[i]['end'] == '1':
            endStops.append(i)

    # print(endStops)
    radiobutton1.setText('от ' + busStops[endStops[1] - 1]['stops'] + ' до ' + busStops[endStops[0]]['stops'])
    radiobutton2.setText('от ' + busStops[endStops[0] + 1]['stops'] + ' до ' + busStops[endStops[1]]['stops'])


def initParser():
    fields = ['game_path', 'login', 'password', 'openDoor', 'voice', 'warnDoor', 'routeInfo', 'welcome']
    checkFields = ['stuffCheck','welcomeCheck', 'routeCheck', 'useInfoCheck']
    for field in fields:
        try:
            parser.get('NOKD', field)
        except NoOptionError:
            parser.set('NOKD', field, '')

    for field in checkFields:
        try:
            parser.get('NOKD', field)
        except NoOptionError:
            parser.set('NOKD', field, 'False')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
