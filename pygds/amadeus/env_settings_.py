# This is a duplicated module. To remove after healthy import
from dotenv import load_dotenv
import os
from pathlib import Path

_DOT_ENV_LOADED = False  # To know if the load is done


def is_loaded():
    """
        Tells wether or not the dot env is loaded
    """
    return _DOT_ENV_LOADED


def load_all():
    """
        Loads all env variables from the .env file
    """
    if not is_loaded():
        env_path = Path('../') / '.env'
        load_dotenv(dotenv_path=env_path)
        global _DOT_ENV_LOADED
        _DOT_ENV_LOADED = True


def get_setting(key: str, default_value=None):
    """
        Retrieve a setting by a given key and ensuring that the dot env is loaded.
        If the setting is not found, use the default value if given.
    """
    if not is_loaded():
        load_all()
    return os.getenv(key, default_value)


if __name__ == "__main__":
    print('is_loaded: {is_loaded()}')
    load_all()
    print('is_loaded: {is_loaded()}')
