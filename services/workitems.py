import logging
from typing import Any, Callable

import requests

from configurations.azdo_settings import Azdo_Settings
from utils.data_cache import DataCache
from utils.data_utils import divide_chunks

data_cache = DataCache()


def get_ids(kind: str) -> list[str]:
    """Get all ids for a work item kind.

    :param kind: The work item kind.
    :return: A list of work item identifiers.
    """
    logger = logging.getLogger(__name__)
    settings = Azdo_Settings.model_validate({})
    logger.debug(f"[BEGIN] Fetching {kind} ids")

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

        logger.debug(f"[END] Fetching {kind} ids")
        return [str(work_item["id"]) for work_item in work_items]

    logger.error(f"Error fetching {kind} ids: {response.text}")
    raise ValueError(response.text)


def fetch_work_items(item_ids: list[str], creator: Callable) -> list[Any]:
    """Return a list of work items.

    :param item_ids: The work item identifiers to fetch.
    :param creator: The function to use to create the work item.
    :return: A list of work items.
    """
    settings = Azdo_Settings.model_validate({})
    logger = logging.getLogger(__name__)
    logger.debug(f"[BEGIN] Fetching work items {item_ids}")

    ids = ",".join(item_ids)
    url = f"{settings.get_rest_base_uri()}/wit/workitems?ids={ids}&$expand=Relations"  # noqa E501
    response = requests.get(
        url,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        logger.debug(f"[END] Fetching work items {item_ids}")
        return [
            creator(val, settings.get_name_discard_str())
            for val in response.json()["value"]
        ]

    logger.error(f"Error fetching work items {item_ids}: {response.text}")
    raise ValueError(response.text)


def get_all_items(kind: str, creator: Callable) -> list[Any]:
    """Return all work items of a given kind.

    :param kind: The work item kind.
    :param creator: The function to use to create the work item.
    :return: A list of work items.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"[BEGIN] Fetching all {kind}")
    items = data_cache.get(kind)  # type: ignore
    if items:
        logger.debug(f"Found {kind} in cache")
        return items

    item_ids = get_ids(kind=kind)
    items: list[Any] = []

    for chunk in divide_chunks(item_ids, 200):
        items += fetch_work_items(item_ids=chunk, creator=creator)

    logger.debug(f"Cache {kind}.")
    data_cache.push(key=kind, value=items)

    logger.debug(f"[END] Fetching all {kind}")
    return items
