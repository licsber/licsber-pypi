import time

from bs4 import BeautifulSoup as bs4
from requests.compat import urljoin

from licsber.spider import get_session
from .paddle_utils import predict_captcha
from .wisedu_utils import need_captcha, check_captcha, get_captcha, encrypt


def get_wisedu_session(url, no, pwd, captcha_retry=99, remember_me=True, custom_session=None):
    """
    对接"金智教务统一登录系统"的API.
    :param url: 访问跳转登录页的url, 通常以authserver开头.
    :param no: 学号.
    :param pwd: 密码.
    :param captcha_retry: 默认验证码重试次数(准确率90%以上).
    :param remember_me: 是否勾选免登录.
    :param custom_session: 自定义session 用于支持vpn.
    :return: 一个登录完成的session, 可以继续访问接下来的网页.
    """

    def retry(session):
        nonlocal pwd_error

        require_captcha = need_captcha(url, session, no)
        captcha = ''
        if require_captcha:
            while not check_captcha(captcha):
                content = get_captcha(url, session)
                captcha = predict_captcha(content)

        res = session.get(url)
        origin_cookie_nums = len(session.cookies)

        data = {
            'lt': None,
            'dllt': None,
            'execution': None,
            '_eventId': None,
            'rmShown': None,
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
        if remember_me:
            data['rememberMe'] = 'on'
        if require_captcha:
            data['captchaResponse'] = captcha

        res = session.post(login_url, data=data)
        if '您提供的用户名或者密码有误' in res.text:
            print(f"{no}: 密码错误.")
            pwd_error = True

        return len(session.cookies) != origin_cookie_nums

    s = custom_session if custom_session else get_session()

    pwd_error = False
    while captcha_retry and not retry(s):
        if pwd_error:
            break

        print(f"{no}: 登录失败 重试中.")
        captcha_retry -= 1
        time.sleep(0.05 * captcha_retry)

    return s
