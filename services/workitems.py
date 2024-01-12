import logging
from typing import Any, Callable

import requests

from configurations.azdo_settings import Azdo_Settings
from utils.data_cache import DataCache
from utils.data_utils import divide_chunks

data_cache = DataCache()


def get_ids(settings: Azdo_Settings, kind: str) -> list[str]:
    logging.info(f"[STARTED] Fetching {kind} ids")

    # api_params = "&".join([f"{k}={v}" for k, v in cfg_api.VERSION.items()])
    url = f"{settings.get_rest_base_uri()}/wit/wiql?$top=5000"
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
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        work_items = response.json()["workItems"]

        logging.info(f"[COMPLETED] Fetching {kind} ids")
        return [str(work_item["id"]) for work_item in work_items]

    logging.error(f"Error fetching {kind} ids: {response.text}")
    raise ValueError(response.text)


def fetch_work_items(
    settings: Azdo_Settings, item_ids: list[str], creator: Callable
) -> list[Any]:
    logging.info(f"[STARTED] Fetching work items {item_ids}")

    ids = ",".join(item_ids)
    url = f"{settings.get_rest_base_uri()}/wit/workitems?ids={ids}&$expand=Relations"  # noqa E501
    response = requests.get(
        url,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        logging.info(f"[COMPLETED] Fetching work items {item_ids}")
        return [
            creator(val, settings.get_name_discard_str())
            for val in response.json()["value"]
        ]

    logging.error(f"Error fetching work items {item_ids}: {response.text}")
    raise ValueError(response.text)


def get_all_items(settings: Azdo_Settings, kind: str, creator: Callable) -> list[Any]:
    logging.info(f"[STARTED] Fetching all {kind}")
    items = data_cache.get(kind)
    if items:
        logging.info(f"Found {kind} in cache")
        return items

    item_ids = get_ids(settings=settings, kind=kind)
    items: list[Any] = []

    for chunk in divide_chunks(item_ids, 200):
        items += fetch_work_items(settings=settings, item_ids=chunk, creator=creator)

    logging.info(f"Cache {kind}.")
    data_cache.push(key=kind, value=items)

    logging.info(f"[COMPLETED] Fetching all {kind}")
    return items
