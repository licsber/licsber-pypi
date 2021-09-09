import os

import torch
import torchvision as tv

from licsber.dl import DATASETS_ROOT

DATASETS_PATH = os.path.join(DATASETS_ROOT, 'pytorch/cifar10')


def cifar10_loader(transform=None, batch_size=256, workers=2):
    if not transform:
        transform = tv.transforms.Compose([
            tv.transforms.ToTensor(),
            tv.transforms.Normalize(
                (0.5, 0.5, 0.5),
                (0.5, 0.5, 0.5),
            ),
        ])

    # download为True就会打印信息 不想让它打印额外信息
    gz_path = os.path.join(DATASETS_PATH, 'cifar-10-python.tar.gz')
    download = not os.path.exists(gz_path)

    train_datasets = tv.datasets.CIFAR10(DATASETS_PATH, download=download, transform=transform)
    test_datasets = tv.datasets.CIFAR10(DATASETS_PATH, train=False, transform=transform)

    kwargs = {
        'batch_size': batch_size,
        'num_workers': workers,
        'pin_memory': True,
    }
    # noinspection PyUnresolvedReferences
    train_loader = torch.utils.data.DataLoader(train_datasets, shuffle=True, **kwargs)
    # noinspection PyUnresolvedReferences
    test_loader = torch.utils.data.DataLoader(test_datasets, shuffle=False, **kwargs)

    return train_loader, test_loader
