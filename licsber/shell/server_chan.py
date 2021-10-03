import argparse

from licsber.github import get_secret
from licsber.spider import get_session


def sct_send(send_key: str, title: str, text: str = ''):
    if not send_key:
        send_key = get_secret('SCT_KEY')

    if not send_key:
        print('SCT_KEY不能为空.')
        exit(-1)

    if len(title) > 32:
        print(f"标题大于32字符: {title}")
        text = title + '\n\n' + text
        title = title[:32]

    data = {
        'title': title,
        'desp': text,
    }

    url = f"https://sctapi.ftqq.com/{send_key}.send"
    s = get_session()
    res = s.post(url, data=data)
    return res


def sct():
    key = get_secret('SCT_KEY')
    if not key:
        print('请设置SCT_KEY环境变量.')
        exit(-1)

    parser = argparse.ArgumentParser(description='推送Server酱.')
    parser.add_argument('title')
    parser.add_argument('desp', nargs='?', default='Licsber: 换行记得使用两个\\n.\n\n永远爱你.')
    args = parser.parse_args()
    sct_send(key, args.title, args.desp)
