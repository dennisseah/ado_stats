from statistics.base import aggr_accumulated, aggr_state, lifecycle
from typing import Any

from pydantic import BaseModel

from configurations.azdo_settings import Azdo_Settings
from services.features import fetch as fetch_features
from services.user_stories import fetch as fetch_user_stories
from utils.display import Table, as_table_group


class UserStoriesStatus(BaseModel):
    new: int = 0
    active: int = 0
    closed: int = 0


def count_user_stories_states(features: list[Any], settings: Azdo_Settings):
    feature_titles = {f.id: f.title for f in features}
    feature_states = {f.id: f.state for f in features}

    user_stories = fetch_user_stories(settings)
    existing_features = {f.id for f in features}
    feature_ids = {f: UserStoriesStatus() for f in existing_features}

    for us in filter(lambda us: us.parent_id, user_stories):
        if us.parent_id in existing_features:
            status = feature_ids.get(us.parent_id)
            if status:
                if us.state == "New":
                    status.new += 1
                elif us.state == "Active":
                    status.active += 1
                else:
                    status.closed += 1

    data = [
        (
            f,
            feature_titles.get(f),
            feature_states.get(f),
            status.new,
            status.active,
            status.closed,
        )
        for f, status in feature_ids.items()
    ]
    data.sort(key=lambda x: x[0])
    return Table(
        title="User Stories States",
        tbl_note="*New, Active, Closed are its user stories' states.*",
        headers=["Id", "Feature Title", "State", "New", "Active", "Closed"],
        data=data,
    )


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    features = fetch_features(settings)

    tables = [
        aggr_state(title="By States", data=features),
        lifecycle(title="Counts", data=features),
        aggr_accumulated(title="Accumulated", data=features),
    ]

    tables.append(count_user_stories_states(features=features, settings=settings))

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
