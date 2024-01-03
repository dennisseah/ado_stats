from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.tasks import fetch as fetch_tasks
from utils.display import as_table_group


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    tasks = fetch_tasks(settings)

    tables = [
        aggr_state(title="By States", data=tasks),
        lifecycle(title="Counts", data=tasks),
        aggr_accumulated(title="Accumulated", data=tasks),
    ]

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
