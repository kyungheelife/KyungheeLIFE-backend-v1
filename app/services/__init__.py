from datetime import datetime


def timestamp() -> float:
    now = datetime.now()
    unix_timestamp = datetime.timestamp(now)
    return unix_timestamp


__all__ = ["timestamp"]
