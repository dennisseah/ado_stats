import logging

from models.feature import Feature
from services.workitems import get_all_items


def fetch() -> list[Feature]:
    """Return a list of all Features.

    :return: list of Features
    """
    logger = logging.getLogger(__name__)
    logger.debug("[BEGIN] Fetching all Features")

    results = get_all_items(kind="Feature", creator=Feature.from_data)

    logger.debug(f"[END] Fetching all Features, found {len(results)} items")
    return results
