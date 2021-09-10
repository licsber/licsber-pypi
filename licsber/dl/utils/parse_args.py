import argparse


class Args:
    def __init__(self, args):
        self.args = args
        self.batch_size = args.batch_size
        self.epochs = args.epochs
        self.lr = args.lr
        self.momentum = args.momentum
        self.workers = args.workers
        self.print_freq = args.print_freq
        self.gpu = args.gpu
        self.device = f'cuda:{self.gpu}' if self.gpu != -1 else 'cpu'
        self.start = args.start
        self.resume = args.resume

    def __str__(self):
        return str(self.args)

    def __repr__(self):
        return self.__class__.__name__ + str(self)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='深度学习 - Parser - By Licsber.')
    parser.add_argument('-b', '--batch-size', default=256, type=int,
                        metavar='N',
                        help='mini-batch size (default: 256), this is the total '
                             'batch size of all GPUs on the current node when '
                             'using Data Parallel or Distributed Data Parallel')
    parser.add_argument('--epochs', default=90, type=int, metavar='N',
                        help='number of total epochs to run')
    parser.add_argument('--lr', '-l', '--learning-rate', default=0.1, type=float,
                        metavar='LR', help='initial learning rate', dest='lr')
    parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                        help='momentum')
    parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                        help='number of data loading workers (default: 4)')
    parser.add_argument('-p', '--print-freq', default=10, type=int,
                        metavar='N', help='print frequency (default: 10)')
    parser.add_argument('--gpu', default=0, type=int,
                        help='GPU id to use.')
    parser.add_argument('--start', default=0, type=int,
                        help='Epochs to be resumed.')
    parser.add_argument('--resume', '-r', action='store_true',
                        help='resume from checkpoint')
    args = parser.parse_args(args)
    return Args(args)
