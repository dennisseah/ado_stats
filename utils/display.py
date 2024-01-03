import streamlit as st
from pydantic import BaseModel
from tabulate import tabulate


class Table(BaseModel):
    title: str
    headers: list[str]
    data: list[tuple]

    def to_dict(self):
        return {h: [x[i] for x in self.data] for i, h in enumerate(self.headers)}

    def to_dataframe(self):
        import pandas as pd

        return pd.DataFrame(self.to_dict())


def as_table(table: Table, tablefmt="fancy_grid"):
    print()
    print(table.title)
    print(tabulate(table.data, headers=table.headers, tablefmt=tablefmt))


def as_table_group(
    group_name: str,
    tables: list[Table],
    tablefmt="fancy_grid",
    tabs: bool = False,
    streamlit: bool = False,
):
    if streamlit:
        if tabs:
            tab_objs = st.tabs([tbl.title for tbl in tables])

            for i, tab in enumerate(tab_objs):
                with tab_objs[i]:
                    st.dataframe(
                        data=tables[i].to_dataframe(),
                        hide_index=True,
                        width=600,
                        height=800,
                    )
        else:
            for tbl in tables:
                st.subheader(tbl.title)
                st.dataframe(
                    data=tbl.to_dataframe(), hide_index=True, width=600, height=800
                )
    else:
        print()
        print(group_name)
        print("-" * len(group_name))

        for tbl in tables:
            print()
            print(tbl.title)
            print(tabulate(tbl.data, headers=tbl.headers, tablefmt=tablefmt))
