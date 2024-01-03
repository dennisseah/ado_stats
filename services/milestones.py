import logging

import requests

import configurations.api as cfg_api
from configurations.azdo_settings import Azdo_Settings
from models.milestone import Milestone
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch(
    settings: Azdo_Settings,
) -> list[Milestone]:
    logging.info("[STARTED] Fetching milestone")

    milestones = data_cache.get("milestone")
    if milestones:
        logging.info("Found milestones in cache")
        return milestones

    url = f"{settings.get_rest_base_uri()}/work/teamsettings/iterations"
    params: dict[str, str] = cfg_api.VERSION
    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        return [Milestone.from_data(r) for r in response.json()["value"]]

    logging.error(f"Error fetching milestones: {response.text}")
    raise ValueError("Cannot fetch data")
