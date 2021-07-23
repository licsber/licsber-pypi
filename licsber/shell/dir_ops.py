import os
import shutil

from licsber.utils import Meta
from licsber.utils import cal_time
from licsber.utils.file_utils import fun_check_path_exist, walk_files


def _all_filepath(start_path):
    for filename in os.listdir(start_path):
        filepath = os.path.join(start_path, filename)
        if os.path.isfile(filepath):
            yield filepath


def _save_file(save_path, filename, text):
    with open(os.path.join(save_path, filename), 'w') as f:
        f.write(text)


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def save_115_link(start_path=None):
    res = ''
    for filepath in _all_filepath(start_path):
        meta = Meta(filepath)
        res += meta.gen_115_link() + '\n'

    _save_file(start_path, '115_links.txt', res)


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def rename(start_path=None):
    for filepath in _all_filepath(start_path):
        meta = Meta(filepath)
        suffix = os.path.splitext(filepath)[1]
        sha1 = meta.sha1()
        dst_name = f"{sha1}.{suffix}" if not suffix.startswith('.') else f"{sha1}{suffix}"
        dst_path = os.path.join(start_path, dst_name if suffix else sha1)
        os.rename(filepath, dst_path)


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def archive(start_path=None):
    res = 'Key,Filename,Size,SHA1,CRC32\n'
    for filepath in _all_filepath(start_path):
        filepath = os.path.relpath(filepath)
        meta = Meta(filepath)
        basename, size, sha1, crc32 = meta.meta()
        res += f'"{filepath}","{basename}",{size},{sha1},{crc32}\n'

    _save_file(start_path, 'tree.licsber.csv', res)


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def flatten_dir(start_path=None):
    all = []
    walk_files(all, start_path)

    start_len = len(start_path)
    for i in all:
        dst = i[start_len + 1:]
        dst = dst.replace(os.sep, '-')
        dst = os.path.join(start_path, dst)
        os.rename(i, dst)
        print(f"移动: {dst}")

    for i in os.listdir(start_path):
        path = os.path.join(start_path, i)
        if os.path.isdir(path):
            print(f"删除: {path}")
            shutil.rmtree(path)


@cal_time(output=True)
@fun_check_path_exist()
def count_dir(start_path=None):
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

    _walk(start_path)
    print(f'共有{nums["dir"]}个子目录.')
    print(f'共有{nums["file"]}个文件.')


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def empty_dir(start_path=None):
    """
    递归删除空文件夹, 如果当前目录删除完也是空的, 一起删除.
    :param start_path: 开始路径.
    """

    count = 0
    all_dirs = []
    for root, _, _ in os.walk(start_path, topdown=False):
        all_dirs.append(root)

    for root in all_dirs:
        if not os.listdir(root):
            count += 1
            print(f"删除目录: {root}")
            os.rmdir(root)

    print(f"共删除{count}个空目录.")
