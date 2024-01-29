from statistics.base import aggr_accumulated, aggr_state, lifecycle

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import utils.aggr_utils as aggr_utils
from services.user_stories import fetch as fetch_stories
from utils.display import Table, as_table_group


def pie_chart(df: pd.DataFrame):
    """Display a pie chart.

    :param df: The data frame.
    """
    data = df.to_dict("list")
    fig = plt.figure(figsize=(4, 3))
    plt.pie(
        data["count"],
        labels=data["points"],
        autopct="%1.1f%%",
        textprops={"fontsize": 5},
    )
    st.pyplot(fig.figure, use_container_width=False)


def generate(title: str, streamlit: bool = False):
    """Generate statistics for user stories.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    user_stories = fetch_stories()

    orphan_stories = [
        (us.id, us.title) for us in filter(lambda us: not us.parent_id, user_stories)
    ]

    tables = [
        aggr_state(title="By States", data=user_stories),
        lifecycle(title="Counts", data=user_stories),
        aggr_accumulated(title="Accumulated", data=user_stories),
        Table(
            title="By Story Points",
            headers=["points", "count"],
            data=aggr_utils.aggr_count(user_stories, "story_points"),
            streamlit_chart=pie_chart,
        ),
        Table(title="Orphaned Stories", headers=["id", "title"], data=orphan_stories),
    ]

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
