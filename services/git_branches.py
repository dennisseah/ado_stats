import logging

import requests

import configurations.api as cfg_api
from configurations.azdo_settings import Azdo_Settings
from models.git_branch import GitBranch
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch(
    settings: Azdo_Settings,
    repo: str,
) -> list[GitBranch]:
    logging.info(f"[STARTED] Fetching branches for {repo}")

    branches = data_cache.get(f"Git Branches {repo}")
    if branches:
        logging.info(f"Found branches for {repo} in cache")
        return branches

    url = f"{settings.get_rest_base_uri()}/git/repositories/{repo}/refs"
    params: dict[str, str | int] = {
        **cfg_api.VERSION,
        **{
            "$top": 200,
            "filter": "heads/",
        },
    }

    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        branches = [
            GitBranch.from_data(
                repo=repo, data=d, discard_name_str=settings.get_name_discard_str()
            )
            for d in response.json()["value"]
        ]
        logging.info(f"Cache branches for {repo}.")
        data_cache.push(key=f"Git Branches {repo}", value=branches)

        logging.info(f"[COMPLETED] Fetching branches for {repo}")
        return branches

    logging.error(f"Error fetching branches for {repo}: {response.text}")
    raise ValueError("Cannot fetch data")
