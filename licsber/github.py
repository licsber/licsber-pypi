import os


def is_ci() -> bool:
    return 'CI' in os.environ


def get_secret(name) -> str:
    return os.environ[name] if name in os.environ else None
