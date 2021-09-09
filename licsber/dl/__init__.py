import os

from .bbox import xywh_to_xyxy
from .bbox import xyxy_to_xywh
from .map_into import map_into
from ..github import get_secret

DATASETS_ROOT = get_secret('DATASETS_ROOT')
CHECKPOINT_ROOT = get_secret('CHECKPOINT_ROOT')

if not DATASETS_ROOT:
    DATASETS_ROOT = '/datasets/'

if not CHECKPOINT_ROOT:
    CHECKPOINT_ROOT = '/datasets/checkpoint/'

for d in [DATASETS_ROOT, CHECKPOINT_ROOT]:
    if not os.path.exists(d):
        os.mkdir(d)
