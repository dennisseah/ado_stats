import logging

from models.task import Task
from services.workitems import get_all_items


def fetch() -> list[Task]:
    """Return a list of all Tasks.

    :return: list of Tasks
    """
    logger = logging.getLogger(__name__)
    logger.debug("[BEGIN] Fetching all Tasks")
    results = get_all_items(kind="Task", creator=Task.from_data)
    logger.debug(f"[END] Fetching all Tasks, found {len(results)} items")
    return results
