import requests

from configurations.azdo_settings import Azdo_Settings
from models.user_story import UserStory


def divide_chunks(data: list[str], n):
    for i in range(0, len(data), n):
        yield data[i : i + n]


def get_story_ids(settings: Azdo_Settings):
    url = f"{settings.get_rest_base_uri()}/wit/wiql?api-version=7.0&$top=5000"
    filter = "[System.WorkItemType] = 'User Story'"
    area_paths = settings.get_area_paths()

    if area_paths:
        paths = "','".join(area_paths)
        filter += f" AND [System.AreaPath] In ('{paths}')"

    body = {"query": f"""
            SELECT [System.Id], [System.Title], [System.AreaPath] FROM WorkItems
            WHERE {filter} ORDER BY [System.ChangedDate] DESC"""}

    response = requests.post(
        url,
        auth=("", settings.azdo_pat),
        json=body,
    )

    if response.status_code == 200:
        work_items = response.json()["workItems"]
        return [str(work_item["id"]) for work_item in work_items]

    raise ValueError(response.text)


def fetch_work_items(settings: Azdo_Settings, item_ids: list[str]) -> list[UserStory]:
    ids = ",".join(item_ids)
    url = f"{settings.get_rest_base_uri()}/wit/workitems?ids={ids}&$expand=Relations&api-version=7.0"  # noqa E501
    response = requests.get(url, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        return [UserStory.from_data(val) for val in response.json()["value"]]

    raise ValueError(response.text)


def get_user_stories(settings: Azdo_Settings) -> list[UserStory]:
    item_ids = get_story_ids(settings)
    user_stories = []

    for chunk in divide_chunks(item_ids, 200):
        user_stories += fetch_work_items(settings, chunk)

    return user_stories
