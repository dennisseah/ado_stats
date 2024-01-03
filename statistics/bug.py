from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.bugs import fetch as fetch_bugs
from utils.display import as_table_group


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    bugs = fetch_bugs(settings)

    tables = [
        aggr_state(title="By States", data=bugs),
        lifecycle(title="Counts", data=bugs),
        aggr_accumulated(title="Accumulated", data=bugs),
    ]

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
