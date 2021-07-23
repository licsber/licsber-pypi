from licsber.utils import uimg


def imshow(*args, **kwargs):
    """
    保持兼容性
    """
    return uimg.imshow(*args, **kwargs)
