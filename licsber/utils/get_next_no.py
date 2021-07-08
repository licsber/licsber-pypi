import os


def get_next_no(path):
    ds_store_path = os.path.join(path, '.DS_Store')
    if os.path.exists(ds_store_path):
        os.remove(ds_store_path)

    all_file = os.listdir(path)
    all_file.sort()
    return int(all_file[-1].split('.')[0]) if all_file else 0
