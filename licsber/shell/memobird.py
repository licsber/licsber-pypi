import argparse

from licsber.notice.memobird import send_text_message


def memobird():
    parser = argparse.ArgumentParser(description='发送信息给咕咕机.')
    parser.add_argument('ak')
    parser.add_argument('device_id')
    parser.add_argument('text', nargs='?', default='Hello from Licsber.')
    args = parser.parse_args()

    send_text_message(args.ak, args.device_id, args.text)
