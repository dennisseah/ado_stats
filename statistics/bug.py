from statistics.base import aggr_accumulated, aggr_state, lifecycle

from services.bugs import fetch as fetch_bugs
from utils.display import as_table_group


def generate(title: str, streamlit: bool = False):
    """Generate statistics for bugs.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    bugs = fetch_bugs()

    tables = [
        aggr_state(title="By States", data=bugs),
        lifecycle(title="Counts", data=bugs),
        aggr_accumulated(title="Accumulated", data=bugs),
    ]

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
