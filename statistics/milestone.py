from collections import defaultdict

from tabulate import tabulate

from configurations.azdo_settings import Azdo_Settings
from models.user_story import UserStory
from services.user_stories import fetch as fetch_stories


def aggr_milestones(data: list[UserStory]):
    milestones = defaultdict(int)

    for story in data:
        milestones[story.milestone] += (
            story.story_points if story.story_points > 0 else 3
        )

    results = [(k, v) for k, v in milestones.items()]
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def generate(settings: Azdo_Settings):
    user_stories = [
        x
        for x in fetch_stories(settings)
        if x.milestone and x.state != "Removed" and x.assigned_to is not None
    ]
    points = aggr_milestones(data=user_stories)
    print("Story points by milestone")
    print(
        tabulate(
            tabular_data=points,
            headers=["milestone", "points"],
            tablefmt="fancy_grid",
        )
    )
