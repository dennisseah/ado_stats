from typing import Iterator


def divide_chunks(data: list[str], n) -> Iterator[list[str]]:
    """Divide a list into chunks of size n.

    :param data: The list to divide.
    :param n: The size of each chunk.
    return The list of chunks.
    """
    for i in range(0, len(data), n):
        yield data[i : i + n]
