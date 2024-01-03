def divide_chunks(data: list[str], n):
    for i in range(0, len(data), n):
        yield data[i : i + n]
