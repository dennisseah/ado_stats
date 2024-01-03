from collections import defaultdict

from configurations.azdo_settings import Azdo_Settings
from models.milestone import Milestone
from models.user_story import UserStory
from services.milestones import fetch as fetch_milestones
from services.user_stories import fetch as fetch_stories
from utils.display import Table, as_table_group


def get_milestones(settings: Azdo_Settings) -> dict[str, Milestone]:
    milestones = fetch_milestones(settings)
    return {x.path: x for x in milestones}


def aggr_milestones(data: list[UserStory], milestones: dict[str, Milestone]):
    points = defaultdict(int)

    for story in data:
        points[story.milestone] += story.story_points if story.story_points > 0 else 3

    results = []
    for mstone, points in points.items():
        ms = milestones.get(mstone)
        if ms:
            results.append((ms.name, str(ms.start_date), str(ms.finish_date), points))
        else:
            results.append((mstone, "", "", points))

    results.sort(key=lambda x: (x[1], x[0]))
    return results


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    user_stories = [
        x
        for x in fetch_stories(settings)
        if x.milestone
        and (x.state == "Closed" or x.state == "Resolved" or x.state == "Active")
    ]

    points = aggr_milestones(data=user_stories, milestones=get_milestones(settings))
    as_table_group(
        group_name=title,
        tables=[
            Table(
                title="Story points by milestone",
                headers=["milestone", "start", "finish", "points"],
                data=points,
            )
        ],
        streamlit=streamlit,
    )
