import requests
from bs4 import BeautifulSoup as bs4
from requests.compat import urljoin

from licsber.auth.wisedu_utils import encrypt


def get_wisedu_session(url, no, pwd):
    """
    对接"金智教务统一登录系统"的API.
    :param url: 访问跳转登录页的url, 通常以authserver开头.
    :param no: 学号.
    :param pwd: 密码.
    :return: 一个登录完成的session, 可以继续访问接下来的网页.
    """
    s = requests.session()
    res = s.get(url)
    data = {
        "lt": None,
        "dllt": None,
        "execution": None,
        "_eventId": None,
        "rmShown": None,
        'pwdDefaultEncryptSalt': None
    }

    res = bs4(res.content, 'html.parser')

    salt = res.find('input', id='pwdDefaultEncryptSalt')['value']
    login_url = res.find('form', id='casLoginForm')['action']
    login_url = urljoin(url, login_url)

    for i in res.find_all('input'):
        if 'name' in i.attrs and i['name'] in data:
            data[i['name']] = i['value']

    data['username'] = no
    data['password'] = encrypt(pwd, salt)

    s.post(login_url, data=data)
    return s
