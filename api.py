# -*- coding: utf-8 -*-

from urllib.error import HTTPError

import requests

domain = 'http://nokd.ru'

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
    url = domain + '/API/methods.php?class=User&method=isDataValidate&username=' + username + '&password=' + password
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

def userNickname(username):
    url = domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=nickname'
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
    url = domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=server'
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

def userOrganisation(username):
    url = domain + '/API/methods.php?class=User&method=get&username=' + username + '&param=organization'
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

def getBuses(username):
    url = domain + '/API/methods.php?class=User&method=getBus&username=' + username
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        #print(response.text)
        return response.text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

def getRoutes(username):
    url = domain + '/API/methods.php?class=Routes&method=get&username=' + username
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

def startWork(username, route, graphic):
    url = domain + '/API/methods.php?class=User&method=setStatus&username=' + username + '&route=' + route + \
          '&station=569&graphic=' + graphic + '&x=-100&y=-100'
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

def endWork(username, deltaTime):
    url = domain + '/API/methods.php?class=User&method=endWork&username=' + username + '&races=1&racesTime=' + deltaTime
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

def updateWork(username, x, y):
    url = domain + '/API/methods.php?class=User&method=updateStatus&username=' + username + '&x='+x+'&y='+y
    print(url)
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