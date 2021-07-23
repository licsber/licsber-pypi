import functools
import inspect
import os
import sys


def check_path_exist(start=None):
    if not start:
        start = os.getcwd() if len(sys.argv) == 1 else os.path.join(os.getcwd(), sys.argv[1])

    if not os.path.exists(start):
        print(f'目录 {start} 不存在, 请检查.')
        exit(-1)

    start = os.path.abspath(start)
    return start


def clean_macos(start):
    for root, dirs, files in os.walk(start):
        for i in files:
            filepath = os.path.join(root, i)
            if not os.path.isfile(filepath):
                continue

            meta_path = os.path.join(root, '._' + i)
            if i == '.DS_Store':
                os.remove(filepath)
                print(f"删除.DS_Store: {root}")
            elif os.path.exists(meta_path):
                meta = open(meta_path, 'rb').read()
                if b'This resource fork intentionally left blank' in meta:
                    os.remove(meta_path)
                    print(f"删除元文件: {meta_path}")


def fun_check_path_exist(arg_name='start_path', clean=False, print_path=True):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            path = kwargs[arg_name] if hasattr(kwargs, arg_name) else None
            path = check_path_exist(path)

            sign = inspect.signature(fun)
            if sign.parameters[arg_name].default != inspect.Parameter.empty:
                kwargs[arg_name] = path

            if print_path:
                print(f'传入目录: {path}')

            if clean:
                clean_macos(path)

            return fun(*args, **kwargs)

        return wrapper

    return decorator


def all_filepath(start_path):
    for filename in os.listdir(start_path):
        filepath = os.path.join(start_path, filename)
        if os.path.isfile(filepath):
            yield filepath


def walk_files(res: list, start_path):
    """
    传入一个list, 递归遍历start_path, 向list中添加文件路径.
    """
    for i in os.listdir(start_path):
        path = os.path.join(start_path, i)
        if os.path.isdir(path):
            walk_files(res, path)
        else:
            res.append(path)


@fun_check_path_exist(arg_name='save_path', print_path=False)
def save_file(save_path, filename, text):
    """
    忽略这个函数 库中代码减少行数使用 也为了方便调试
    """
    with open(os.path.join(save_path, filename), 'w') as f:
        f.write(text)
