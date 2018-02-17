from datetime import datetime, timedelta


def get_utc_datetime(date, *args, **kwargs):
    if isinstance(date, datetime):
        return date.isoformat()
    else:
        return datetime(date, *args, **kwargs).isoformat()


def date_range(start_date, day_count):
    for n in range(day_count):
        yield start_date + timedelta(n)
