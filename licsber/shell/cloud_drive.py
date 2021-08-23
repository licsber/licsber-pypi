import hashlib
import json
import os
import sys

from licsber.utils.ufile import fun_check_path_exist, save_file
from licsber.utils.umeta import Meta
from licsber.utils.utime import cal_time


@cal_time(output=True)
@fun_check_path_exist(clean=True)
def save_115_dir(start_path=None):
    if os.path.isfile(start_path):
        meta = Meta(start_path)
        print(meta)
        return

    if not os.path.isdir(start_path):
        print(f"选定目录错误: {start_path}")
        return

    save_json_name = 'licsber-bak.json'
    save_path = os.path.join(start_path, save_json_name)
    if os.path.exists(save_path):
        print(f"已存在归档文件: {save_path}")
        sha1_obj = hashlib.sha1()
        sha1_obj.update(open(save_path, 'rb').read())
        print(f"归档文件sha1: {sha1_obj.hexdigest().upper()}")
        dst_path = os.path.join(start_path, 'licsber-bak-old.json')
        os.rename(save_path, dst_path)

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
                # 去除威联通QNAP-NAS中的缓存文件夹
                if os.path.basename(path) in {'.@__thumb', '@Recycle', '@Transcode'}:
                    continue

                exists_path = os.path.join(path, save_json_name)
                if os.path.exists(exists_path):
                    dir_info = json.load(open(exists_path))
                else:
                    dir_info = build(path)

                node['dirs'].extend([dir_info])
            elif os.path.isfile(path):
                if os.path.basename(path) in {save_json_name, 'licsber-bak-old.json'}:
                    continue

                meta = Meta(path)
                node['files'].append(meta.link_115.lstrip('115://'))
                node['baidu'].append(meta.link_baidu)

        return node

    res = build(start_path)
    dir_info = json.dumps(res)
    sha1_obj = hashlib.sha1()
    sha1_obj.update(dir_info.encode())
    print(f"归档文件sha1: {sha1_obj.hexdigest().upper()}")
    save_file(start_path, save_json_name, dir_info)


@cal_time(output=True)
@fun_check_path_exist()
def conv(start_path=None):
    """
    兼容格式如下:
    https://github.com/orzogc/fake115uploader
    :param start_path:
    :return:
    """
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
