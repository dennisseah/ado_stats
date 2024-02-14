from typing import Any

import pandas as pd
import streamlit as st

from utils.aggr_utils import aggr_count, merge
from utils.display import Table


def aggr_state(title: str, data: list[Any]) -> Table:
    """Aggregates the states of the given data.

    :param title: The title of the table.
    :param data: The data to be aggregated.
    :return: The aggregated data.
    """
    import matplotlib.pyplot as plt
    import pandas as pd
    import streamlit as st

    def pie_chart(df: pd.DataFrame):
        data = df.to_dict("list")
        fig = plt.figure(figsize=(4, 3))
        plt.pie(
            data["count"],
            labels=data["state"],
            autopct="%1.0f%%",
            textprops={"fontsize": 4.5},
        )
        st.pyplot(fig.figure, use_container_width=False)

    results = aggr_count(data=data, dimension="state", include_percentage=True)

    return Table(
        title=title,
        headers=["state", "count", "percentage"],
        data=results,
        streamlit_chart=pie_chart,
    )


def aggr_accumulated(title: str, data: list[Any]) -> Table:
    """Aggregates the accumulated data of the given data.

    :param title: The title of the table.
    :param data: The data to be aggregated.
    :return: Display table object.
    """
    aggr_created = aggr_count(data, "created_week", sort_values=False)
    aggr_closed = aggr_count(data, "closed_week", sort_values=False)
    aggr_removed = aggr_count(
        [x for x in data if x.state == "Removed"],
        "changed_week",
        sort_values=False,
    )

    removed = {x[0]: x[1] for x in aggr_removed}
    closed = {x[0]: x[1] for x in aggr_closed}

    created_weeks = [x[0] for x in aggr_created]
    for x in removed.keys():
        if x not in created_weeks:
            aggr_created.append((x, 0))

    created_weeks = [x[0] for x in aggr_created]
    for x in closed.keys():
        if x not in created_weeks:
            aggr_created.append((x, 0))

    aggr_created.sort(key=lambda x: x[0])

    results = []
    accumulated = 0

    for created in aggr_created:
        accumulated += (
            created[1] - closed.get(created[0], 0) - removed.get(created[0], 0)
        )
        results.append(
            (
                created[0],
                created[1],
                closed.get(created[0], 0),
                removed.get(created[0], 0),
                accumulated,
            )
        )

    def plot_line_chart(df: pd.DataFrame):
        st.line_chart(df, x="year - week", y="accumulated")

    return Table(
        title=title,
        headers=[
            "year - week",
            "# created",
            "# closed",
            "# removed",
            "accumulated",
        ],
        data=results,
        streamlit_chart=plot_line_chart,
    )


def lifecycle(title: str, data: list[Any]) -> Table:
    """Returns lifecycle of the given data.

    :param title: The title of the table.
    :param data: The data to be aggregated.
    :return: Display table object.
    """
    created_by = aggr_count(data=data, dimension="created_by")
    assigned = aggr_count(data=data, dimension="assigned_to")
    closed_by = aggr_count(data=data, dimension="closed_by")
    removed_by = aggr_count([us for us in data if us.state == "Removed"], "changed_by")
    merged = merge(data=[created_by, assigned, closed_by, removed_by])
    merged.sort(key=lambda x: x[1], reverse=True)

    return Table(
        title=title,
        headers=["engineer", "created", "assigned", "closed", "removed"],
        data=merged,
    )
