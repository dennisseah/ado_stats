from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.tasks import fetch as fetch_tasks


def generate(settings: Azdo_Settings):
    tasks = fetch_tasks(settings)

    aggr_state(title="Task by states", data=tasks)
    lifecycle(title="Task Counts", data=tasks)
    aggr_accumulated(title="Accumulated tasks", data=tasks)
