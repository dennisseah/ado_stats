import streamlit as st
from pydantic import BaseModel
from tabulate import tabulate


class Table(BaseModel):
    title: str
    headers: list[str]
    data: list[tuple]

    def to_dict(self):
        return {h: [x[i] for x in self.data] for i, h in enumerate(self.headers)}


def as_table_group(
    group_name: str, tables: list[Table], tablefmt="fancy_grid", streamlit: bool = False
):
    if streamlit:
        for tbl in tables:
            st.subheader(tbl.title)
            st.table(tbl.to_dict())
    else:
        print()
        print(group_name)
        print("-" * len(group_name))

        for tbl in tables:
            print()
            print(tbl.title)
            print(tabulate(tbl.data, headers=tbl.headers, tablefmt=tablefmt))
