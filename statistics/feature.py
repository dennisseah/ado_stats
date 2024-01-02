from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.features import fetch as fetch_features
from utils.display import as_table_group


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    features = fetch_features(settings)

    tables = [
        aggr_state(title="Feature by states", data=features),
        lifecycle(title="Feature Counts", data=features),
        aggr_accumulated(title="Accumulated features", data=features),
    ]

    as_table_group(group_name=title, tables=tables, streamlit=streamlit)
