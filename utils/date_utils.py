from datetime import datetime


def to_date(date_str: str | None) -> datetime | None:
    """Converts the given date string to datetime.

    :param date_str: The date string.
    :return: The datetime.
    """
    if not date_str:
        return None

    idx = date_str.find(".")
    return datetime.strptime(date_str[0:idx] + "Z", "%Y-%m-%dT%H:%M:%SZ")


def to_week(d: datetime | None) -> str | None:
    """Converts the given datetime to week.

    :param d: The datetime.
    :return: The week.
    """
    if not d:
        return None

    week = str(d.isocalendar().week)
    week = "0" + week if len(week) == 1 else week
    return f"{d.year} - {week}"
