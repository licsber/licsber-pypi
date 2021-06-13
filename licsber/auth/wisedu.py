from bs4 import BeautifulSoup as bs4
from requests.compat import urljoin

from licsber.auth.paddle_utils import predict_captcha
from licsber.auth.wisedu_utils import check_captcha
from licsber.auth.wisedu_utils import encrypt
from licsber.auth.wisedu_utils import get_captcha
from licsber.auth.wisedu_utils import need_captcha
from licsber.spider import get_session


def get_wisedu_session(url, no, pwd, captcha_retry=3):
    """
    对接"金智教务统一登录系统"的API.
    :param url: 访问跳转登录页的url, 通常以authserver开头.
    :param no: 学号.
    :param pwd: 密码.
    :return: 一个登录完成的session, 可以继续访问接下来的网页.
    """

    def retry(session):
        require_captcha = need_captcha(url, session, no)
        captcha = ''
        if require_captcha:
            while not check_captcha(captcha):
                content = get_captcha(url, session)
                captcha = predict_captcha(content)

        res = session.get(url)
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

        data['rememberMe'] = 'on'
        data['username'] = no
        data['password'] = encrypt(pwd, salt)
        if require_captcha:
            data['captchaResponse'] = captcha

        session.post(login_url, data=data)
        return len(session.cookies) != 2

    s = get_session()
    while captcha_retry and not retry(s):
        captcha_retry -= 1

    return s
