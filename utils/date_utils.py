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


def to_date_str(d: datetime | None) -> str:
    """Converts the given datetime to string Year-Month-day.

    :param d: The datetime.
    :return: formatted date string.
    """
    if not d:
        return ""
    month = f"0{d.month}" if d.month < 10 else f"{d.month}"
    day = f"0{d.day}" if d.day < 10 else f"{d.day}"
    return f"{d.year}-{month}-{day}"
