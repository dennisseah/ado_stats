from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.bugs import fetch as fetch_bugs
from utils.display import as_table_group


def generate(settings: Azdo_Settings):
    bugs = fetch_bugs(settings)

    tables = [
        aggr_state(title="Bug by states", data=bugs),
        lifecycle(title="Bug Counts", data=bugs),
        aggr_accumulated(title="Accumulated bugs", data=bugs),
    ]

    as_table_group(group_name="Bugs", tables=tables)
