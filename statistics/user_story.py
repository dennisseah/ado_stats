from statistics.base import aggr_accumulated, aggr_state, lifecycle

import utils.aggr_utils as aggr_utils
from configurations.azdo_settings import Azdo_Settings
from services.user_stories import fetch as fetch_stories
from utils.display import as_table


def generate(settings: Azdo_Settings):
    user_stories = fetch_stories(settings)

    aggr_state(title="User Stories by states", data=user_stories)
    lifecycle(title="User Story Counts", data=user_stories)
    aggr_accumulated(title="Accumulated User Stories", data=user_stories)

    as_table(
        title="User Stories by story points",
        headers=["points", "count"],
        data=aggr_utils.aggr_count(user_stories, "story_points"),
    )
