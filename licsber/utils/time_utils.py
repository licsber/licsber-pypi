import random
import time


def get_now_date() -> str:
    """
    获取当前本地日期, 格式为[2020-12-12].
    :return: 当前本地日期
    """
    now_time = time.localtime()
    return time.strftime('%Y-%m-%d', now_time)


def get_timestamp() -> int:
    """
    获取1970年到现在UTC的秒数.
    :return: 自1970年1月1日 0点0分0秒以来的秒数.
    """
    now_time = time.time()
    return int(now_time)


def get_timestamp_mil() -> int:
    """
    获取1970年到现在UTC的秒数.
    :return: 自1970年1月1日 0点0分0秒以来的秒数.
    """
    now_time = time.time() * 1000 + random.randint(0, 999)
    return int(now_time)


def get_timestamp_str() -> str:
    """
    获取当前本地时间, 格式为[2020-12-12 11:22:33].
    :return: 当前本地时间
    """
    now_time = time.localtime()
    return time.strftime('%Y-%m-%d %H:%M:%S', now_time)


def cal_time(output=False, fps=False):
    """
    计算函数运行时间, 以秒为单位.
    :param output: 是否print输出.
    :param fps: 是否输出fps, 而不是秒数.
    :return: (out, res) 其中res为函数返回值. 当res为None时只返回None.
    """

    def decorator(fun):
        def wrapper(*args, **kwargs):
            last = time.time()
            res = fun(*args, **kwargs)
            real_time = time.time() - last
            if output:
                if fps:
                    print(f"FPS: {1 / real_time:.2f}")
                else:
                    print(f"执行时间: {real_time:.2f}s")
            if not res:
                return None
            return real_time, res

        return wrapper

    return decorator
