import os

import torch
import torchvision as tv

from licsber.dl import DATASETS_ROOT

DATASETS_PATH = os.path.join(DATASETS_ROOT, 'pytorch/cifar10')

CLASSES = (
    'plane', 'car', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
)


def loader(transform_train=None, transform_test=None, batch_size=256, workers=2, pin_memory=True):
    if not transform_train:
        transform_train = tv.transforms.Compose([
            tv.transforms.RandomCrop(32, padding=4),
            tv.transforms.RandomHorizontalFlip(),
            tv.transforms.ToTensor(),
            tv.transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ])

    if not transform_test:
        transform_test = tv.transforms.Compose([
            tv.transforms.ToTensor(),
            tv.transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ])

    # download为True就会打印信息 不想让它打印额外信息
    gz_path = os.path.join(DATASETS_PATH, 'cifar-10-python.tar.gz')
    download = not os.path.exists(gz_path)

    train_datasets = tv.datasets.CIFAR10(DATASETS_PATH, download=download, transform=transform_train)
    test_datasets = tv.datasets.CIFAR10(DATASETS_PATH, train=False, transform=transform_test)

    kwargs = {
        'batch_size': batch_size,
        'num_workers': workers,
        'pin_memory': pin_memory,
    }
    # noinspection PyUnresolvedReferences
    train_loader = torch.utils.data.DataLoader(train_datasets, shuffle=True, **kwargs)
    # noinspection PyUnresolvedReferences
    test_loader = torch.utils.data.DataLoader(test_datasets, shuffle=False, **kwargs)

    return train_loader, test_loader
