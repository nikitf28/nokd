# -*- coding: utf-8 -*-

from urllib.error import HTTPError

import requests

import settings

domain = settings.domain
pwd = settings.pwd


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


def login(username, password):
    domain = settings.domain
    pwd = settings.pwd
    url = domain + '/API/methods.php?class=User&method=isDataValidate&username=' + username + '&password=' + password + pwd
    try:
        #print(url)
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def userNickname(username):
    url = domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=nickname' + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        #print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def userServer(username):
    url = domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=server' + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def userOrganisation(username):
    url = domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=organization' + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def getBuses(username):
    url = domain + '/API/methods.php?class=User&method=getBus&username=' + username + pwd
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def getRoutes(username):
    url = domain + '/API/methods.php?class=Routes&method=get&username=' + username + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def startWork(username, route, graphic):
    url = domain + '/API/methods.php?class=User&method=setStatus&username=' + username + '&route=' + route + \
          '&station=569&graphic=' + graphic + '&x=-100&y=-100' + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:

        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def endWork(username, deltaTime):
    url = domain + '/API/methods.php?class=User&method=endWork&username=' + username + '&races=1&racesTime=' \
          + deltaTime + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def updateWork(username, x, y):
    url = domain + '/API/methods.php?class=User&method=updateStatus&username=' + username + '&x=' + x + '&y=' + y + pwd
    # print(url)
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def getVersion():
    global domain
    global pwd
    domain = settings.domain
    pwd = settings.pwd
    url = domain + '/API/methods.php?class=Program&method=getVersion&pass=0a773ea7cb61f3d1655d731ff6507dc47b5481f4' \
          + pwd
    # print(url)
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def getOrgName(orgID):
    url = domain + '/API/methods.php?class=Org&method=getName&id=' + orgID + '&param=organization' + pwd
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def countStat():
    url = 'http://notalive.ru/NOKDbusStatLogin'
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        # print(response.text)
        return  False
    except HTTPError as http_err:
        return True
    except Exception as err:
        return True
    else:
        return False
