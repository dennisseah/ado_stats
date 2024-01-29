from typing import Callable

import altair as alt
import pandas as pd
import streamlit as st
from pydantic import BaseModel
from tabulate import tabulate


class Table(BaseModel):
    title: str
    headers: list[str]
    data: list[tuple]
    tbl_note: str | None = None
    streamlit_chart: Callable | None = None

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
    def streamlit_tbl(tbl: Table):
        st.markdown(f"**{tbl.title}**")
        if tbl.streamlit_chart:
            tbl.streamlit_chart(tbl.to_dataframe())  # type: ignore

        if tbl.tbl_note:
            st.markdown(tbl.tbl_note)
        st.dataframe(
            data=tbl.to_dataframe(),
            hide_index=True,
            width=600,
            height=min(800, 50 * len(tbl.data)),
        )

    if streamlit:
        if tabs:
            tab_objs = st.tabs([tbl.title for tbl in tables])

            for i, tab in enumerate(tab_objs):
                with tab:
                    streamlit_tbl(tables[i])
        else:
            for tbl in tables:
                streamlit_tbl(tbl)

    else:
        print()
        print(group_name)
        print("-" * len(group_name))

        for tbl in tables:
            print()
            print(tbl.title)
            if tbl.tbl_note:
                print(tbl.tbl_note)
            print(tabulate(tbl.data, headers=tbl.headers, tablefmt=tablefmt))


def plot_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    value_vars: list[str],
):
    src = df.melt(id_vars=[x_column], value_vars=value_vars)

    chart = (
        alt.Chart(src)
        .mark_bar(strokeWidth=100)
        .encode(
            x=alt.X(
                "variable:N", title="", scale=alt.Scale(paddingOuter=0.5), axis=None
            ),
            y="value:Q",
            color=alt.Color(
                "variable:N",
                legend=alt.Legend(
                    orient="top",
                ),
            ),
            column=alt.Column(f"{x_column}:N", title="", spacing=0),
        )
        .configure_header(labelOrient="bottom")  # type: ignore
    )

    st.altair_chart(chart, use_container_width=False)
