from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.bugs import fetch as fetch_bugs


def generate(settings: Azdo_Settings):
    bugs = fetch_bugs(settings)

    print("Bug by states")
    aggr_state(data=bugs)

    print("Contributors to bugs")
    lifecycle(data=bugs)

    print("Accumulated bugs")
    aggr_accumulated(data=bugs)
