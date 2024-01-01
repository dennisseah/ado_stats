from pydantic import BaseModel
from tabulate import tabulate


class Table(BaseModel):
    title: str
    headers: list[str]
    data: list[tuple]


def as_table(table: Table, tablefmt="fancy_grid"):
    print()
    print(table.title)
    print(tabulate(table.data, headers=table.headers, tablefmt=tablefmt))


def as_table_group(group_name: str, tables: list[Table], tablefmt="fancy_grid"):
    print()
    print(group_name)
    print("-" * len(group_name))

    for tbl in tables:
        as_table(tbl, tablefmt=tablefmt)
