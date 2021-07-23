import os
import sys

import tqdm

from licsber.utils.ufile import fun_check_path_exist, all_filepath, save_file
from licsber.utils.umeta import Meta
from licsber.utils.utime import cal_time


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def save_115_link(start_path=None):
    res = ''
    waiting = list(all_filepath(start_path))
    waiting.sort()
    for filepath in tqdm.tqdm(waiting):
        meta = Meta(filepath)
        res += meta.gen_115_link() + '\n'

    save_file(start_path, '115_links.txt', res)


@cal_time(output=True)
@fun_check_path_exist()
def conv(start_path=None):
    if not os.path.isfile(start_path):
        print(f"需要传入合法的115link文件: {start_path}")
        exit(-1)

    dirname = os.path.dirname(start_path)
    root_name = os.path.basename(dirname)
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
