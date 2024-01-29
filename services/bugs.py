from models.bug import Bug
from services.workitems import get_all_items


def fetch():
    """Return a list of all Bugs."""
    return get_all_items(kind="Bug", creator=Bug.from_data)
