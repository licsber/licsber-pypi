import os
import shutil
import sys

from licsber.utils import cal_time


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


@cal_time(output=True)
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


@cal_time(output=True)
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


@cal_time(output=True)
def empty_dir(start=None):
    """
    递归删除空文件夹, 如果当前目录删除完也是空的, 一起删除.
    :param start: 开始路径.
    :return:
    """
    start = _check_exist(start)

    count = 0
    all_dirs = []
    for root, dirs, files in os.walk(start, topdown=False):
        for i in files:
            if i == '.DS_Store':
                os.remove(os.path.join(root, i))
                print(f"删除.DS_Store: {root}")
        all_dirs.append(root)

    for root in all_dirs:
        if not os.listdir(root):
            count += 1
            print(f"删除目录: {root}")
            os.rmdir(root)

    print(f"共删除{count}个空目录.")


def clean_ds_store(start):
    for root, dirs, files in os.walk(start):
        for i in files:
            if i == '.DS_Store':
                print(f"删除.DS_Store: {root}")
                os.remove(os.path.join(root, i))
