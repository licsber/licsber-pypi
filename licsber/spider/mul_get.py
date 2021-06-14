import queue
import random
import threading
import time
from queue import Empty
from typing import List

import requests

from .session import get_session


def _get_content(session: requests.Session, url: str, timeout: int):
    res = session.get(url, timeout=timeout)
    if res.status_code == 200:
        return res.content
    if res.status_code == 404:
        return b'Error, 404.'
    if res.status_code == 403:
        return b'Error, 403.'
    if res.status_code == 400:
        return b'Error, 400.'
    raise Exception(res.status_code)


def _loop(session: requests.Session,
          req_queue: queue.Queue,
          res: list,
          timeout: int, delay: int):
    if not session:
        session = get_session()

    while not req_queue.empty():
        time.sleep(delay * random.randint(1, 5))
        try:
            url = req_queue.get(block=False)
        except Empty:
            print(f"{threading.current_thread()}: finished.")
            break

        try:
            content = _get_content(session, url, timeout)
        except requests.exceptions.ConnectionError:
            print(f"{url}: Connection err.")
            res.append((url, b'Error, Connection err.'))
            req_queue.task_done()
            continue
        except Exception as e:
            print(f"{url}: Read time out or failure: {e}.")
            req_queue.put(url)
            req_queue.task_done()
            continue

        print(f"{threading.current_thread()}: finish {url}.")
        res.append((url, content))
        req_queue.task_done()


def mul_get_content(urls: List[str],
                    workers_num: int = 32,
                    delay: int = 0.5,
                    session: requests.Session = None,
                    timeout: int = 2) -> List[(str, bytes)]:
    """
    多线程发送GET请求，获取URL内容。
    常用于批量爬取页面，下载图片等用途。
    :param urls: 下载链接列表。
    :param workers_num: 开启线程数。
    :param delay: 等待基准时间 避免爬取过快 单位s.
    :param session: 是否使用统一的session。
    :param timeout: 默认超时等待时间。
    :return: (url, content)形式的列表。
    """
    req_queue = queue.Queue()
    for i in urls:
        req_queue.put(i)

    res = []
    for i in range(workers_num):
        th = threading.Thread(
            target=_loop,
            args=(session, req_queue, res, timeout, delay),
        )
        th.start()

    req_queue.join()
    return res
