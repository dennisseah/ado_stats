from statistics.base import aggr_accumulated, aggr_state, lifecycle

from services.tasks import fetch as fetch_tasks
from utils.display import as_table_group


def generate(title: str, streamlit: bool = False):
    """Generate statistics for tasks.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    tasks = fetch_tasks()

    tables = [
        aggr_state(title="By States", data=tasks),
        lifecycle(title="Counts", data=tasks),
        aggr_accumulated(title="Accumulated", data=tasks),
    ]

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
