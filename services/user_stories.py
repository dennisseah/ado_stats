from models.user_story import UserStory
from services.workitems import get_all_items


def fetch() -> list[UserStory]:
    """Return a list of all User Stories."""
    return get_all_items(kind="User Story", creator=UserStory.from_data)
