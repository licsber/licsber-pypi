from pathlib import Path

from .bbox import xywh_to_xyxy
from .bbox import xyxy_to_xywh
from .map_into import map_into
from ..github import get_secret

DATASETS_ROOT = get_secret('DATASETS_ROOT', '/datasets/')
CHECKPOINT_ROOT = get_secret('CHECKPOINT_ROOT', '/datasets/checkpoint/')

DATASETS_ROOT = Path(DATASETS_ROOT)
CHECKPOINT_ROOT = Path(CHECKPOINT_ROOT)
DATASETS_ROOT.mkdir(exist_ok=True)
CHECKPOINT_ROOT.mkdir(exist_ok=True)
