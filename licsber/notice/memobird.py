import requests

from licsber.utils import get_timestamp_str
from licsber.utils import to_gbk_base64

URLS = {
    'set_user_bind': 'https://open.memobird.cn/home/setuserbind',
    'print_paper': 'https://open.memobird.cn/home/printpaper',
    'get_print_status': 'https://open.memobird.cn/home/getprintstatus'
}


def set_user_bind(ak: str, device_id: str, identifying='licsber') -> str:
    params = {
        'ak': ak,
        'timestamp': get_timestamp_str(),
        'memobirdID': device_id,
        'useridentifying': identifying,
    }
    res = requests.post(URLS['set_user_bind'], params=params).json()
    if res['showapi_res_code'] != 1:
        print(res)
        return ''
    return str(res['showapi_userid'])


def send_text_message(ak: str, device_id: str, text: str, userid=None) -> str:
    params = {
        'ak': ak,
        'timestamp': get_timestamp_str(),
        'printcontent': 'T:' + to_gbk_base64(text),
        'memobirdID': device_id,
        'userID': userid if userid else set_user_bind(ak, device_id, device_id),
    }
    res = requests.post(URLS['print_paper'], params=params).json()
    if res['showapi_res_code'] != 1:
        print(res)
        return ''
    return res['printcontentid']


def get_status(ak: str, print_id: str) -> str:
    params = {
        'ak': ak,
        'timestamp': get_timestamp_str(),
        'printcontentid': print_id,
    }
    res = requests.post(URLS['get_print_status'], params=params).json()
    if res['showapi_res_code'] != 1:
        print(res)
        return ''
    return res['printflag']
