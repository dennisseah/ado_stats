from tabulate import tabulate


def as_table(title: str, headers: list[str], data: list[tuple]):
    print()
    print(title)
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
