import base64


def to_gbk_base64(utf8: str) -> str:
    return base64.b64encode(utf8.encode('gbk')).decode()
