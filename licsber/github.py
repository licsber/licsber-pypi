import os


def is_ci() -> bool:
    """
    判断当前环境是否是Github Actions.
    :return: 是否处在CI环境.
    """
    return 'CI' in os.environ


def get_secret(name) -> str:
    """
    获取Github Secrets中的参数.
    实际上是环境变量.
    :param name: 环境变量名称.
    :return: 字符串类型的环境变量值.
    """
    return os.environ[name] if name in os.environ else None
