from statistics.base import aggr_accumulated, aggr_state, lifecycle

from tabulate import tabulate

import utils.aggr_utils as aggr_utils
from configurations.azdo_settings import Azdo_Settings
from services.user_stories import fetch as fetch_stories


def generate(settings: Azdo_Settings):
    user_stories = fetch_stories(settings)

    print("User Stories by states")
    aggr_state(data=user_stories)

    print("Contributors to user stories")
    lifecycle(data=user_stories)

    print("Accumulated User Stories")
    aggr_accumulated(user_stories)

    print("User Stories by story points")
    print(
        tabulate(
            tabular_data=aggr_utils.aggr_count(user_stories, "story_points"),
            headers=["points", "count"],
            tablefmt="fancy_grid",
        )
    )
