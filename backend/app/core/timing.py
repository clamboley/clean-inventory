import datetime

DEFAULT_TIMEZONE = datetime.UTC

def get_current_time() -> datetime.datetime:
    """Get the current time in the default timezone."""
    return datetime.datetime.now(tz=DEFAULT_TIMEZONE)
