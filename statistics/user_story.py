from statistics.base import aggr_accumulated, aggr_state, lifecycle

import utils.aggr_utils as aggr_utils
from configurations.azdo_settings import Azdo_Settings
from services.user_stories import fetch as fetch_stories
from utils.display import Table, as_table_group


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    user_stories = fetch_stories(settings)

    tables = [
        aggr_state(title="By States", data=user_stories),
        lifecycle(title="Counts", data=user_stories),
        aggr_accumulated(title="Accumulated", data=user_stories),
        Table(
            title="By Story Points",
            headers=["points", "count"],
            data=aggr_utils.aggr_count(user_stories, "story_points"),
        ),
    ]

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
