from collections import defaultdict
from datetime import datetime

import pandas as pd
import streamlit as st

from models.milestone import Milestone
from services.milestones import fetch as fetch_milestones
from services.user_stories import fetch as fetch_stories
from utils.display import Table, as_table_group


def get_milestones() -> dict[str, Milestone]:
    """Get milestones.

    :return: dict of identifier to milestone
    """
    milestones = fetch_milestones()
    return {x.path: x for x in milestones}


def aggr_milestones() -> list[tuple[str, str, str, str, int, int]]:
    """Aggregate story points by milestone.

    :param milestones: The list of milestones.
    :return: The aggregated story points.
    """
    milestones = get_milestones()
    user_stories = [x for x in fetch_stories() if x.milestone]

    def fmt_date(d: datetime | None) -> str:
        return d.strftime("%Y-%m-%d") if d else ""

    points = {
        "open": defaultdict(int),
        "closed": defaultdict(int),
    }

    for story in user_stories:
        if story.state == "Closed" or story.state == "Resolved":
            points["closed"][story.milestone] += (
                story.story_points if story.story_points > 0 else 5
            )
        else:
            points["open"][story.milestone] += (
                story.story_points if story.story_points > 0 else 5
            )

    def fmt_point(id: str, milestone: Milestone) -> tuple[str, str, str, str, int, int]:
        return (
            milestone.name,
            milestone.timeframe,
            fmt_date(milestone.start_date),
            fmt_date(milestone.finish_date),
            points["open"].get(id, 0),
            points["closed"].get(id, 0),
        )

    results = [fmt_point(id, milestone) for id, milestone in milestones.items()]
    results.sort(key=lambda x: (x[2], x[0]))
    return results


def plot_chart(df: pd.DataFrame):
    """Plot burndown chart.

    :param df: The data frame.
    """
    st.markdown("Burndown chart")
    st.area_chart(df, x="milestone", y=["active", "resolved"])


def generate(title: str, streamlit: bool = False):
    """Generate statistics for milestones.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """

    points = aggr_milestones()
    tbl = Table(
        title="Story points by milestone",
        headers=["milestone", "state", "start", "finish", "active", "resolved"],
        data=points,
        streamlit_chart=plot_chart,
    )

    as_table_group(group_name=title, tables=[tbl], streamlit=streamlit)
