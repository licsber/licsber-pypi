import os

DATASETS_PATH = os.path.join(os.environ['HOME'], '.licsber')
if not os.path.exists(DATASETS_PATH):
    os.mkdir(DATASETS_PATH)

from .setu_1024 import SeTu1024
