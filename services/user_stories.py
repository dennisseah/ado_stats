from configurations.azdo_settings import Azdo_Settings
from models.user_story import UserStory
from services.workitems import get_all_items


def fetch(settings: Azdo_Settings) -> list[UserStory]:
    return get_all_items(
        settings=settings, kind="User Story", creator=UserStory.from_data
    )
