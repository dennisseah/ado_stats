from typing import Any, Callable

import requests

from configurations.azdo_settings import Azdo_Settings


def divide_chunks(data: list[str], n):
    for i in range(0, len(data), n):
        yield data[i : i + n]


def get_ids(settings: Azdo_Settings, kind: str) -> list[str]:
    url = f"{settings.get_rest_base_uri()}/wit/wiql?api-version=7.0&$top=5000"
    filter = f"[System.WorkItemType] = '{kind}'"
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


def fetch_work_items(
    settings: Azdo_Settings, item_ids: list[str], creator: Callable
) -> list[Any]:
    ids = ",".join(item_ids)
    url = f"{settings.get_rest_base_uri()}/wit/workitems?ids={ids}&$expand=Relations&api-version=7.0"  # noqa E501
    response = requests.get(url, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        return [creator(val) for val in response.json()["value"]]

    raise ValueError(response.text)


def get_all_items(settings: Azdo_Settings, kind: str, creator: Callable) -> list[Any]:
    item_ids = get_ids(settings=settings, kind=kind)
    items: list[Any] = []

    for chunk in divide_chunks(item_ids, 200):
        items += fetch_work_items(settings=settings, item_ids=chunk, creator=creator)

    return items
