import json
import os
import sys

import tqdm

from licsber.utils.ufile import fun_check_path_exist, all_filepath, save_file
from licsber.utils.umeta import Meta
from licsber.utils.utime import cal_time


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def save_115_link(start_path=None):
    """
    预计将要废弃 请使用save-115-dir这个更好用的命令
    :param start_path: 
    :return:
    """
    if os.path.isfile(start_path):
        meta = Meta(start_path)
        print(meta)
        return

    res = ''
    waiting = list(all_filepath(start_path))
    waiting.sort()
    for filepath in tqdm.tqdm(waiting):
        meta = Meta(filepath)
        res += meta.get_115_link() + '\n'

    save_file(start_path, '115_links.txt', res)


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def save_115_dir(start_path=None):
    if not os.path.isdir(start_path):
        print(f"选定目录错误: {start_path}")
        return

    save_path = os.path.join(start_path, 'licsber_115.json')
    if os.path.exists(save_path):
        os.remove(save_path)

    def build(root):
        node = {
            'dir_name': os.path.basename(root),
            'dirs': [],
            'files': [],
            'baidu': [],
        }
        for i in os.listdir(root):
            path = os.path.join(root, i)
            if os.path.isdir(path):
                if os.path.basename(path) in {'.@__thumb', '@Recycle', '@Transcode'}:
                    continue

                node['dirs'].extend([build(path)])
            elif os.path.isfile(path):
                meta = Meta(path)
                link = meta.get_115_link().lstrip('115://')
                baidu_link = meta.get_baidu_link()
                node['files'].append(link)
                node['baidu'].append(baidu_link)

        return node

    res = build(start_path)
    save_file(start_path, 'licsber_115.json', json.dumps(res))


@cal_time(output=True)
@fun_check_path_exist()
def conv(start_path=None):
    if not os.path.isfile(start_path):
        print(f"需要传入合法的115link文件: {start_path}")
        exit(-1)

    dirname = os.path.dirname(start_path)
    root_name = 'TMP[Licsber]/' + os.path.basename(start_path).rstrip('.txt')
    root_name = sys.argv[2] if len(sys.argv) == 3 else root_name

    res, line = '', ''
    text = open(start_path).read().strip().split('\n')
    try:
        for line in text:
            filename, size, sha1, block = line.lstrip('115://').split('|')
            res += f"aliyunpan://{filename}|{sha1}|{size}|{root_name}\n"
    except ValueError:
        print(f"115Link不合法: {line}")
        exit(-1)

    save_file(dirname, 'aliyunpan_links.txt', res)
