import queue
import threading
import time

import requests

from .session import get_session


def _get_content(session: requests.Session, url: str, timeout: int):
    res = session.get(url, timeout=timeout)
    if res.status_code != 200:
        raise Exception('Res code error.')
    return res.content


def _loop(session: requests.Session, req_queue: queue.Queue, res: list, timeout: int):
    if not session:
        session = get_session()

    while not req_queue.empty():
        time.sleep(0.1)
        url = req_queue.get()

        try:
            content = _get_content(session, url, timeout)
        except ...:
            print(url + ' Read time out.')
            req_queue.put(url)
            req_queue.task_done()
            continue

        res.append((url, content))
        req_queue.task_done()


def mul_get_content(urls: list[str],
                    workers_num: int = 16,
                    session: requests.Session = None,
                    timeout: int = 3) -> list[(str, bytes)]:
    """
    多线程发送GET请求，获取URL内容。
    常用于批量爬取页面，下载图片等用途。
    :param urls: 下载链接列表。
    :param workers_num: 开启线程数。
    :param session: 是否使用统一的session。
    :param timeout: 默认超时等待时间。
    :return: (url, content)形式的列表。
    """
    req_queue = queue.Queue()
    for i in urls:
        req_queue.put(i)

    res = []
    for i in range(workers_num):
        th = threading.Thread(target=_loop, args=(session, req_queue, res, timeout))
        th.start()
    req_queue.join()
    return res
