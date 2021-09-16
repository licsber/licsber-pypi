import argparse
import os
import sys
from pathlib import Path

from licsber.dl import CHECKPOINT_ROOT


class Args:
    def __init__(self, args):
        self.args = args
        self.save_path = Path(args.save_path)
        self.save_path.mkdir(exist_ok=True)
        self.batch_size = args.batch_size
        self.img_size = args.img_size
        self.epochs = args.epochs
        self.lr = args.lr
        self.momentum = args.momentum
        self.workers = args.workers
        self.print_freq = args.print_freq
        self.gpu = args.gpu
        self.device = f'cuda:{self.gpu}' if self.gpu != -1 else 'cpu'
        self.start_epoch = args.start_epoch
        self.resume = args.resume
        self.pin_memory = args.no_pin_memory

        self.mac = sys.platform == 'darwin'
        if self.mac:
            self.gpu = -1
            self.device = 'cpu'

    def __str__(self):
        return str({
            'save_path': self.save_path,
            'batch_size': self.batch_size,
            'img_size': self.img_size,
            'epochs': self.epochs,
            'lr': self.lr,
            'momentum': self.momentum,
            'workers': self.workers,
            'print_frep': self.print_freq,
            'gpu': self.gpu,
            'device': self.device,
            'start_epoch': self.start_epoch,
            'resume': self.resume,
            'pin_memory': self.pin_memory,
            'mac': self.mac,
        })

    def __repr__(self):
        return self.__class__.__name__ + str(self)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='DeepLearning - Parser - By Licsber.')
    parser.add_argument('--save-path', default=str(CHECKPOINT_ROOT), type=str,
                        metavar='PATH',
                        help='path to save checkpoint')
    parser.add_argument('-b', '--batch-size', default=256, type=int,
                        metavar='N',
                        help='mini-batch size (default: 256), this is the total '
                             'batch size of all GPUs on the current node when '
                             'using Data Parallel or Distributed Data Parallel')
    parser.add_argument('-i', '--img-size', default=224, type=int,
                        metavar='N',
                        help='img square size')
    parser.add_argument('-e', '--epochs', default=1000, type=int, metavar='N',
                        help='number of total epochs to run')
    parser.add_argument('-l', '--lr', '--learning-rate', default=0.1, type=float,
                        metavar='LR', help='initial learning rate', dest='lr')
    parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                        help='momentum')
    parser.add_argument('-j', '--workers', default=os.cpu_count(), type=int, metavar='N',
                        help='number of data loading workers (default: cpu_count)')
    parser.add_argument('-p', '--print-freq', default=10, type=int,
                        metavar='N', help='print frequency (default: 10)')
    parser.add_argument('--gpu', default=0, type=int,
                        help='GPU id to use.')
    parser.add_argument('--start-epoch', default=0, type=int,
                        help='Epochs to be resumed.')
    parser.add_argument('--resume', '-r', action='store_true',
                        help='resume from checkpoint')
    parser.add_argument('--no-pin-memory', action='store_false',
                        help='dont pin memory for dataloader')
    args = parser.parse_args(args)
    return Args(args)


if __name__ == '__main__':
    print(parse_args())
