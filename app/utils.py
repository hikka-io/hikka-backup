from datetime import datetime, UTC
from functools import lru_cache
from dynaconf import Dynaconf


# Replacement for deprecated datetime's utcnow
def utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


@lru_cache()
def get_settings():
    """Returns lru cached system settings"""

    return Dynaconf(
        settings_files=["settings.toml"],
        default_env="default",
        environments=True,
    )


def chunkify(lst, size):
    """Split list into chunks"""
    return [lst[i : i + size] for i in range(0, len(lst), size)]
