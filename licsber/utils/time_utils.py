import time


def get_now_date() -> str:
    """
    获取当前的日期, 格式为[2020-12-12].
    :return: 当前日期
    """
    now_time = time.localtime()
    return time.strftime('%Y-%m-%d', now_time)


def get_timestamp() -> int:
    """
    获取1970年到现在的秒数.
    :return: 自1970年1月1日 0点0分0秒以来的秒数.
    """
    now_time = time.time()
    return int(now_time)
