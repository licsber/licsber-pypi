import sys


def check_force(force=False):
    if force:
        return force

    return '--force' in sys.argv
