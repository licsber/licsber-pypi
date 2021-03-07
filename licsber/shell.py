import argparse
import os
import shutil
import sys


def _check_exist(start):
    if not start:
        start = os.getcwd() if len(sys.argv) == 1 else os.path.join(os.getcwd(), sys.argv[1])

    if not os.path.exists(start):
        print(f'目录 {start} 不存在, 请检查.')
        exit(-1)

    print(f'目录 {start} :')
    return start


def walk_files(res: list, start):
    for i in os.listdir(start):
        path = os.path.join(start, i)
        if os.path.isdir(path):
            walk_files(res, path)
        else:
            res.append(path)


def flatten_dir(start=None):
    start = _check_exist(start)
    start = os.path.abspath(start)

    all = []
    walk_files(all, start)

    start_len = len(start)
    for i in all:
        dst = i[start_len + 1:]
        dst = dst.replace(os.sep, '-')
        dst = os.path.join(start, dst)
        os.rename(i, dst)
        print(f"移动: {dst}")
    for i in os.listdir(start):
        path = os.path.join(start, i)
        if os.path.isdir(path):
            print(f"删除: {path}")
            shutil.rmtree(path)


def count_dir(start=None):
    start = _check_exist(start)
    nums = {
        'file': 0,
        'dir': 0
    }

    def _walk(p):
        for i in os.listdir(p):
            path = os.path.join(p, i)
            if os.path.isdir(path):
                nums['dir'] += 1
                _walk(path)
            else:
                nums['file'] += 1

    _walk(start)
    print(f'共有{nums["dir"]}个子目录.')
    print(f'共有{nums["file"]}个文件.')


def licsber():
    print('Hello, Licsber.')


def memobird():
    from licsber.notice.memobird import send_text_message

    parser = argparse.ArgumentParser(description='发送信息给咕咕机.')
    parser.add_argument('ak')
    parser.add_argument('device_id')
    parser.add_argument('text', nargs='?', default='Hello from Licsber.')
    args = parser.parse_args()

    send_text_message(args.ak, args.device_id, args.text)
