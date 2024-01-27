from collections import defaultdict

import pandas as pd

from configurations.azdo_settings import Azdo_Settings
from models.milestone import Milestone
from models.user_story import UserStory
from services.milestones import fetch as fetch_milestones
from services.user_stories import fetch as fetch_stories
from utils.display import Table, as_table_group, plot_bar_chart


def get_milestones(settings: Azdo_Settings) -> dict[str, Milestone]:
    milestones = fetch_milestones(settings)
    return {x.path: x for x in milestones}


def aggr_milestones(data: list[UserStory], milestones: dict[str, Milestone]):
    points = {
        "open": defaultdict(int),
        "closed": defaultdict(int),
    }

    for story in data:
        if story.state == "Closed" or story.state == "Resolved":
            points["closed"][story.milestone] += (
                story.story_points if story.story_points > 0 else 5
            )
        else:
            points["open"][story.milestone] += (
                story.story_points if story.story_points > 0 else 5
            )

    results = []
    for ms, milestone in milestones.items():
        results.append(
            (
                milestone.name,
                (
                    milestone.start_date.strftime("%Y-%m-%d")
                    if milestone.start_date
                    else ""
                ),
                (
                    milestone.finish_date.strftime("%Y-%m-%d")
                    if milestone.finish_date
                    else ""
                ),
                points["open"].get(ms, 0),
                points["closed"].get(ms, 0),
            )
        )

    results.sort(key=lambda x: (x[1], x[0]))
    return results


def plot_chart(df: pd.DataFrame):
    plot_bar_chart(
        df=df,
        x_column="milestone",
        id_vars=["milestone"],
        value_vars=["active", "resolved"],
    )


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    user_stories = [x for x in fetch_stories(settings) if x.milestone]

    points = aggr_milestones(data=user_stories, milestones=get_milestones(settings))
    tbl = Table(
        title="Story points by milestone",
        headers=["milestone", "start", "finish", "active", "resolved"],
        data=points,
        height=400,
        streamlit_chart=plot_chart,
    )

    as_table_group(group_name=title, tables=[tbl], streamlit=streamlit)
