from models.task import Task
from services.workitems import get_all_items


def fetch():
    """Return a list of all Tasks."""
    return get_all_items(kind="Task", creator=Task.from_data)
