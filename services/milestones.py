import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from models.milestone import Milestone
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch() -> list[Milestone]:
    """Fetch milestones from Azure DevOps

    :return: A list of milestones.
    """
    logging.info("[STARTED] Fetching milestone")
    settings = Azdo_Settings.model_validate({})

    milestones = data_cache.get("milestone")
    if milestones:
        logging.info("Found milestones in cache")
        return milestones

    url = f"{settings.get_rest_base_uri()}/work/teamsettings/iterations"
    response = requests.get(
        url,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        return [Milestone.from_data(r) for r in response.json()["value"]]

    logging.error(f"Error fetching milestones: {response.text}")
    raise ValueError("Cannot fetch data")
