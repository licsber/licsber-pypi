import time


def get_now_date() -> str:
    now_time = time.localtime()
    return time.strftime('%Y-%m-%d', now_time)
