from datetime import datetime


def to_date(date_str: str | None) -> datetime | None:
    if not date_str:
        return None

    idx = date_str.find(".")
    return datetime.strptime(date_str[0:idx] + "Z", "%Y-%m-%dT%H:%M:%SZ")
