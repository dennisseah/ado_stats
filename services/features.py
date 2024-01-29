from models.feature import Feature
from services.workitems import get_all_items


def fetch():
    """Return a list of all Features."""
    return get_all_items(kind="Feature", creator=Feature.from_data)
