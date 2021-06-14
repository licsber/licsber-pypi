import requests
import urllib3
from requests import Session
from requests.adapters import HTTPAdapter

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
}


def get_session(retry_time=5, verify=False, proxies=None, headers=None) -> Session:
    """
    获取预配置session.
    :param retry_time: 重试次数.
    :param verify: 是否验证https证书, 默认不验证, 加速爬虫.
    :param proxies: 设置代理服务器.
    :param headers: 默认请求头.
    :return: Session对象.
    """
    if not verify:
        urllib3.disable_warnings()

    s = requests.Session()

    s.mount('http://', HTTPAdapter(max_retries=retry_time))
    s.mount('https://', HTTPAdapter(max_retries=retry_time))

    s.verify = verify

    if proxies:
        s.proxies.update(proxies)

    if not headers:
        headers = DEFAULT_HEADERS

    s.headers = headers

    return s
