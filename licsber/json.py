from licsber.utils import ujson


def pretty_print(*args, **kwargs):
    """
    保持兼容性
    """
    return ujson.pretty_print(*args, **kwargs)
