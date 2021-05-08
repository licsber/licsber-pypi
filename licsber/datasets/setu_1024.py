import os
import random
from collections import defaultdict

import cv2
import h5py
import numpy as np

from licsber.datasets import DATASETS_PATH
from licsber.shell import clean_ds_store
from licsber.shell import empty_dir
from licsber.utils import cal_time


class SeTu1024:
    def __init__(self,
                 dataset_path=os.path.join(DATASETS_PATH, '1024'),
                 dataset_filename='1024.h5',
                 size=(224, 224)):
        if not os.path.exists(dataset_path):
            os.mkdir(dataset_path)

        self.path = dataset_path
        self.filename = dataset_filename

        self.label = {
            0: 'like',
            1: 'dislike',
        }
        self.items = {
            'like/train': 0,
            'like/test': 0,
            'dislike/train': 1,
            'dislike/test': 1,
        }
        self.size = size

    def make_dataset(self, test_ratio=0.1):
        random.seed(test_ratio)

        clean_ds_store(self.path)
        dir_paths = [os.path.join(self.path, i) for i in self.label.values()]
        for dir_path in dir_paths:
            dirs = ['train', 'test']
            for d in dirs:
                path = os.path.join(dir_path, d)
                if not os.path.exists(path):
                    os.mkdir(path)

            files = os.listdir(dir_path)
            files.remove('train')
            files.remove('test')

            random.shuffle(files)
            test_len = int(len(files) * test_ratio) + 1
            test = files[:test_len]
            for file in test:
                src = os.path.join(dir_path, file)
                dst = os.path.join(dir_path, 'test', file)
                os.rename(src, dst)

            for file in files[test_len:]:
                src = os.path.join(dir_path, file)
                dst = os.path.join(dir_path, 'train', file)
                os.rename(src, dst)

    def reset_dataset(self):
        dir_paths = [os.path.join(self.path, i) for i in self.label.values()]
        for dir_path in dir_paths:
            dirs = ['train', 'test']
            for d in dirs:
                path = os.path.join(dir_path, d)
                if os.path.exists(path):
                    for _, _, files in os.walk(path):
                        for file in files:
                            src = os.path.join(path, file)
                            dst = os.path.join(dir_path, file)
                            os.rename(src, dst)

            empty_dir(dir_path)

    @cal_time(output=True)
    def make_h5(self, save_path=None):
        if not save_path:
            save_path = os.path.join(self.path, self.filename)

        datasets = defaultdict(list)
        labels = defaultdict(list)

        for item in self.items:
            path = os.path.join(self.path, item)
            for img_filename in os.listdir(path):
                img_path = os.path.join(path, img_filename)
                img = cv2.imread(img_path)
                img = cv2.resize(img, self.size)
                label = [self.items[item]]
                if 'test' in item:
                    datasets['test'].append(img)
                    labels['test'].append(label)
                else:
                    datasets['train'].append(img)
                    labels['train'].append(label)

        with h5py.File(save_path, 'w') as h5:
            for d, l in zip(datasets, labels):
                h5.create_dataset(d, data=np.array(datasets[d]))
                h5.create_dataset(l + '_label', data=np.array(labels[l]))

    def load_dataset(self):
        h5_path = os.path.join(self.path, self.filename)
        if not os.path.exists(h5_path):
            print("请先生成数据集文件.")
            return None

        with h5py.File(h5_path) as h5:
            return (h5['train'][:], h5['train_label'][:]), (h5['test'][:], h5['test_label'][:])


def load_dataset():
    return SeTu1024().load_dataset()
