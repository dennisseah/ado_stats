from configurations.azdo_settings import Azdo_Settings
from models.user_story import UserStory
from services.workitems import get_all_items


def divide_chunks(data: list[str], n):
    for i in range(0, len(data), n):
        yield data[i : i + n]


def get_user_stories(settings: Azdo_Settings) -> list[UserStory]:
    return get_all_items(
        settings=settings, kind="User Story", creator=UserStory.from_data
    )
