import pandas as pd
import streamlit as st

from services.user_stories import fetch as fetch_stories
from utils.display import Table, as_table_group


def fetch_data() -> list[tuple[str, int, int]]:
    """Fetch data for burndown chart.

    :return: The data for the burndown chart.
    """
    user_stories = fetch_stories()

    week_ranges = set([us.created_week for us in user_stories])
    week_ranges.update([us.closed_week for us in user_stories if us.closed_week])
    list_weeks = list(week_ranges)
    list_weeks.sort()  # type: ignore

    created: list[int] = []
    completed: list[int] = []

    for wk in list_weeks:
        _created = sum(
            [us.story_points for us in user_stories if us.created_week == wk]
        )
        created.append(_created)
        completed.append(
            _created
            + sum([us.story_points for us in user_stories if us.closed_week == wk])
        )

    aggr_created: list[int] = [created[0]]
    aggr_completed: list[int] = [completed[0]]

    for i in range(1, len(created)):
        aggr_created.append(aggr_created[i - 1] + created[i])
        aggr_completed.append(aggr_completed[i - 1] + completed[i])

    return list(zip(list_weeks, aggr_created, aggr_completed))  # type: ignore


def plot_chart(df: pd.DataFrame):
    """Plot burndown chart.

    :param df: The data frame.
    """
    st.markdown("Burndown chart for story points per sprint")
    st.area_chart(df, x="week", y=["completed", "backlog"])


def generate(title: str, streamlit: bool = False):
    """Generate statistics for burn down.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    try:
        if streamlit:
            with st.expander("information"):
                st.markdown("**Burndown rate**")
                st.markdown(
                    "This chart shows the amount of work that has been completed in a "
                    "sprint, and the total work remaining. Burndown charts are used "
                    "to predict your team's likelihood of completing their work in the "
                    " time available. Here are the guidelines\n"
                    "1. Perform capacity planning\n"
                    "2. Track progress\n"
                    "3. Identify scope creep\n"
                    "4. Identify bottlenecks\n"
                    "5. Understand the team's velocity in completing tasks\n"
                    "6. Inform ensemble's stakeholders of the team's progress, and "
                    "request for more development team when needed.\n"
                )
        points = fetch_data()
        tbl = Table(
            title="Burndown Chart",
            headers=["week", "completed", "backlog"],
            data=points,
            streamlit_chart=plot_chart,
        )

        as_table_group(group_name=title, tables=[tbl], streamlit=streamlit)
    except Exception:
        st.markdown("Error")
