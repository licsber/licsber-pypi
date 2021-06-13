import base64
import random

import requests
from Crypto.Cipher import AES

from licsber.utils import get_timestamp_mil

CAPTCHA_URL = 'http://authserver.njit.edu.cn/authserver/captcha.html'


def pad(s: bytes, block_size: int) -> bytes:
    l = len(s)
    pad_num = block_size - (l % block_size)
    if pad_num == 0:
        pad_num = block_size
    pad_b = bytes([pad_num])
    return s + pad_b * pad_num


def aes_encrypt(s: str, key: str, iv='\0' * 16, coding='utf-8') -> str:
    key_b = key.encode(coding)
    iv_b = iv.encode(coding)
    raw_b = s.encode(coding)

    cipher = AES.new(key_b, AES.MODE_CBC, iv_b)
    padded = pad(raw_b, AES.block_size)
    encrypted = cipher.encrypt(padded)
    encoded = base64.b64encode(encrypted)
    return encoded.decode(coding)


def encrypt(pwd, salt):
    charsets = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    rnd_16 = ''.join(random.choice(charsets) for _ in range(16))
    rnd_64 = ''.join(random.choice(charsets) for _ in range(64))
    return aes_encrypt(rnd_64 + pwd, salt, rnd_16)


def check_captcha(text):
    CHAR_LIST = '12345678ABCDEFHKNPQXYZabcdefhknpxyz'

    if len(text) != 4:
        return False

    for ch in text:
        if ch not in CHAR_LIST:
            return False

    return True


def get_captcha(url: str, session: requests.Session):
    CAPTCHA_URL = url.split('/authserver/')[0] + '/authserver/captcha.html'
    params = {
        'ts': random.randint(1, 999),
    }
    res = session.get(CAPTCHA_URL, params=params)
    return res.content


def need_captcha(url: str, session: requests.Session, no):
    NEED_CAPTCHA_URL = url.split('/authserver/')[0] + '/authserver/needCaptcha.html'
    params = {
        'username': no,
        'pwdEncrypt2': 'pwdEncryptSalt',
        '_': get_timestamp_mil,
    }
    res = session.get(NEED_CAPTCHA_URL, params=params)
    return res.json()
