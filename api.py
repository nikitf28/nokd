# -*- coding: utf-8 -*-

from urllib.error import HTTPError

import requests

import settings


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
    url = settings.domain + '/API/methods.php?class=User&method=isDataValidate&username=' + username + '&password=' + password + settings.pwd
    try:
        # print(url)
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
    url = settings.domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=nickname' + settings.pwd
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


def userServer(username):
    url = settings.domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=server' + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=organization' + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=User&method=getBus&username=' + username + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=Routes&method=get&username=' + username + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=User&method=setStatus&username=' + username + '&route=' + route + \
          '&station=569&graphic=' + graphic + '&x=-100&y=-100' + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=User&method=endWork&username=' + username + '&races=1&racesTime=' \
          + deltaTime + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=User&method=updateStatus&username=' + username + '&x=' + x + '&y=' + y + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=Program&method=getVersion&' \
          + settings.pwd
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
    url = settings.domain + '/API/methods.php?class=Org&method=getName&id=' + orgID + '&param=organization' + settings.pwd
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
        print(response.text)
        if response.text == 'a\n':
            return False
        return True
    except HTTPError as http_err:
        return True
    except Exception as err:
        return True
    else:
        return False


def getStops(route):
    url = settings.domain + '/API/methods.php?class=Routes&method=getInf&number=' + route + settings.pwd
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


def checkAudioDLC(orgID):
    url = settings.domain + '/API/methods.php?class=Org&method=ifDlc&id=' + orgID + '&param=organization' + settings.pwd
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
