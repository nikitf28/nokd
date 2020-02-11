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
from configparser import SafeConfigParser, ConfigParser

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QPushButton, QComboBox, QFileDialog, \
    QMessageBox, QPlainTextEdit


#sys.setdefaultencoding('utf-8')
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
        global gameDir
        gameDir = parser.get('NOKD', 'game_path')
        self.logsBox = QPlainTextEdit()
        self.initUI()

    def closeEvent(self, event):
        api.endWork(username, str((time.process_time() - timeBegin) // 60))

    def initUI(self):
        global loginEdit, passwordEdit, loginStatusText, driverNameText, driverOrganizationText, workButton, \
            breakButton, accidentButton, routeBox, busBox, graphicEdit

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

        driverNameText = QLabel('Водитель:                                ', self)
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
        #busBox.addItem('ПАЗ 32053 №О000ОО77')
        #busBox.addItem('Газель №К777ОТ77')
        #busBox.addItem('МАЗ 203 №С123ТС77')

        busText = QLabel('Маршрут: ', self)
        busText.move(230, 100)
        busText.setFont(defaultFont)
        busBox.setDisabled(True)

        routeBox = QComboBox(self)
        routeBox.setFont(defaultFont)
        routeBox.setGeometry(QRect(300, 100, 60, 20))
        routeBox.setDisabled(True)
        #routeBox.addItem('4')
        #routeBox.addItem('6')
        #routeBox.addItem('К5')
        #routeBox.addItem('ПАРК')

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

        #logsBox.move(230, 150)
        self.logsBox.setGeometry(QRect(230, 150, 100, 100))

        self.setWindowTitle('НОКД - клиент для водителей ЧАТП (' + settings.verString +  ')')
        self.setWindowIcon(QIcon(iconPath))
        self.setFixedSize(600, 260)
        self.show()

        loginAPI()

    def startWork(self):
        if not settings.located_status:
            global timeBegin
            settings.located_status = True
            #accidentButton.setEnabled(True)
            #breakButton.setEnabled(True)
            busBox.setEnabled(False)
            routeBox.setEnabled(False)
            graphicEdit.setEnabled(False)
            workButton.setText('Закончить смену')
            timeBegin = datetime.datetime.now()
            api.startWork(username, routeBox.currentText(), graphicEdit.text())
            thread = location.LocationControl(parent=self, mainWindow = self)
            thread.start()

        else:
            settings.located_status = False
            accidentButton.setEnabled(False)
            breakButton.setEnabled(False)
            graphicEdit.setEnabled(True)
            busBox.setEnabled(True)
            routeBox.setEnabled(True)
            workButton.setText('  Выйти на линию   ')
            api.endWork(username, str((datetime.datetime.now() - timeBegin)//60))


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
        pathErrorBox.setText("Ничего нового. Ты так и не смог найти нужную папку. Повторяю: в этой папке фарминции нет!")
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
        #print(nickName)
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
        #breakButton.setEnabled(True)
        #accidentButton.setEnabled(True)

        busBox.clear()
        buses = json.loads(api.getBuses(loginData))

        routes = json.loads(api.getRoutes(loginData))

        if buses is not None:
            busBox.addItem(api.html_decode(buses['model']+ ' ' + buses['number']))

        routeBox.clear()

        if routes is not None:
            for route in routes:
                routeBox.addItem(api.html_decode(route['number']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
