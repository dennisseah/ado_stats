import logging

from models.user_story import UserStory
from services.workitems import get_all_items


def fetch() -> list[UserStory]:
    """Return a list of all User Stories.

    :return: list of User Stories
    """
    logger = logging.getLogger(__name__)
    logger.debug("[BEGIN] Fetching all User Stories")

    results = get_all_items(kind="User Story", creator=UserStory.from_data)

    logger.debug(f"[END] Fetching all User Stories, found {len(results)} items")
    return results
