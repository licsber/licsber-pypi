import requests

from licsber import get_mongo
from licsber.utils import get_timestamp_str
from licsber.utils import to_gbk_base64

URLS = {
    'set_user_bind': 'https://open.memobird.cn/home/setuserbind',
    'print_paper': 'https://open.memobird.cn/home/printpaper',
    'get_print_status': 'https://open.memobird.cn/home/getprintstatus'
}


def set_user_bind(ak: str, device_id: str, identifying='licsber') -> str:
    """
    绑定userid.
    :param ak: 开发者ak.
    :param device_id: 设备id 双击机器吐出来的.
    :param identifying: 用户自定义字符串.
    :return: 绑定成功的userid, 失败返回空串.
    """
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
    """
    向咕咕机发送纯文本消息.
    :param ak: 开发者ak.
    :param device_id: 设备id 双击机器吐出来的.
    :param text: 文本信息.
    :param userid: 可选的userid.
    :return: 打印id, 失败返回空串.
    """
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
    return str(res['printcontentid'])


def get_status(ak: str, print_id: str) -> str:
    """
    获取消息发送的状态.
    :param ak: 开发者ak.
    :param print_id: 打印接口返回的打印id.
    :return: 已经打印返回1, 失败返回空串.
    """
    params = {
        'ak': ak,
        'timestamp': get_timestamp_str(),
        'printcontentid': print_id,
    }
    res = requests.post(URLS['get_print_status'], params=params).json()
    if res['showapi_res_code'] != 1:
        print(res)
        return ''
    return str(res['printflag'])


def log_message(mongo_passwd_b64: str, message: str):
    """
    生成mongo日志, 偷懒的接口.
    :param mongo_passwd_b64: mongo密码 同get_mongo的参数.
    :param message: 文本信息.
    :return: 插入结果.
    """
    db = get_mongo(mongo_passwd_b64)['memobird']
    return db.insert_one({
        'type': 'plain',
        'text': message,
        'print': False,
    })
