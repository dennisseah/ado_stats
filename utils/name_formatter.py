def format_name(name: str, discard_str: list[str]) -> str:
    for discard in discard_str:
        name = name.replace(discard, "")

    return name.strip()
