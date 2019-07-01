from dotenv import load_dotenv
import os
from pathlib import Path

_DOT_ENV_LOADED = False


def is_loaded():
    return _DOT_ENV_LOADED


def load_all():
    if not is_loaded():
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        global _DOT_ENV_LOADED
        _DOT_ENV_LOADED = True


def get_setting(key: str, default_value=None):
    if not is_loaded():
        load_all()
    return os.getenv(key, default_value)


if __name__ == "__main__":
    print('is_loaded: {is_loaded()}')
    load_all()
    print('is_loaded: {is_loaded()}')
