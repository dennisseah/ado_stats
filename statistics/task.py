from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.tasks import fetch as fetch_tasks


def generate(settings: Azdo_Settings):
    tasks = fetch_tasks(settings)

    print("Task by states")
    aggr_state(data=tasks)

    print("Contributors to tasks")
    lifecycle(data=tasks)

    print("Accumulated tasks")
    aggr_accumulated(data=tasks)
