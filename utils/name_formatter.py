def format_name(name: str, discard_str: list[str]) -> str:
    """Format a name by discarding some strings.

    :param name: The name to format.
    :param discard_str: The strings to discard.
    :return: The formatted name.
    """
    for discard in discard_str:
        name = name.replace(discard, "")

    return name.strip()
