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
    stories = fetch_stories()
    backlogs = set()

    def fmt_date(d: datetime | None) -> str:
        return d.strftime("%Y-%m-%d") if d else ""

    points = {
        "open": defaultdict(int),
        "closed": defaultdict(int),
    }

    for story in stories:
        if story.milestone not in milestones:
            backlogs.add(story.milestone)

        if story.state == "Closed" or story.state == "Resolved":
            points["closed"][story.milestone] += (
                story.story_points if story.story_points > 0 else 5
            )
        else:
            points["open"][story.milestone] += (
                story.story_points if story.story_points > 0 else 5
            )

    def fmt_point(
        id: str, milestone: Milestone | None
    ) -> tuple[str, str, str, str, int, int]:
        return (
            milestone.name if milestone else "backlog",
            milestone.timeframe if milestone else "future",
            fmt_date(milestone.start_date) if milestone else "---",
            fmt_date(milestone.finish_date) if milestone else "---",
            points["open"].get(id, 0),
            points["closed"].get(id, 0),
        )

    results = [fmt_point(id, milestone) for id, milestone in milestones.items()]

    results.sort(key=lambda x: (x[2], x[0]))
    for backlog in backlogs:
        results.append(fmt_point(backlog, None))

    return results


def plot_chart(df: pd.DataFrame):
    """Plot burndown chart.

    :param df: The data frame.
    """
    st.markdown("Story points per sprint")
    st.area_chart(df, x="milestone", y=["active", "resolved"])


def generate(title: str, streamlit: bool = False):
    """Generate statistics for milestones.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    if streamlit:
        with st.expander("guidelines"):
            st.markdown("**Story points per sprint**")
            st.markdown(
                "This are chart shows the story points by milestone. "
                "It shows the active and resolved stories by points."
            )
            st.markdown(
                "The table below shows the same information in tabular form. "
                "The table shows the number of story points for each sprints. "
                "For completed sprints, it shows the number of story points resolved. "
                "For current and future sprints, it shows the number of story points"
                "planned. "
                "It is important to note that the story points are not always accurate "
                "because they are just estimates. During sprint planning, it is "
                "important \n"
                "1. Review the story points and adjust them as necessary.\n"
                "2. Do not over commit during sprint planning, and number of story "
                "points per sprint can provide a good indication of the team's "
                "velocity.\n"
                "3. Do not under commit during sprint planning.\n"
                "4. Development team members should be aware that committed story "
                "for the sprint should be completed by the end of the sprint.\n"
            )
    points = aggr_milestones()
    tbl = Table(
        title="Story points by milestone",
        headers=["milestone", "state", "start", "finish", "active", "resolved"],
        data=points,
        streamlit_chart=plot_chart,
    )

    as_table_group(group_name=title, tables=[tbl], streamlit=streamlit)
