from configurations.azdo_settings import Azdo_Settings
from models.task import Task
from services.workitems import get_all_items


def fetch(settings: Azdo_Settings):
    return get_all_items(settings=settings, kind="Task", creator=Task.from_data)
