import datetime
from time import timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
