import logging

from models.bug import Bug
from services.workitems import get_all_items


def fetch() -> list[Bug]:
    """Return a list of all Bugs.

    :return: list of Bugs
    """
    logger = logging.getLogger(__name__)
    logger.debug("[BEGIN] Fetching all Bugs")

    results = get_all_items(kind="Bug", creator=Bug.from_data)

    logger.debug(f"[END] Fetching all Bugs, found {len(results)} items")
    return results
