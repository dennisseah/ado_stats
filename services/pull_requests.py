import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from models.pull_request import PullRequest
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch_pull_requests(
    settings: Azdo_Settings,
    repo: str,
    active_only: bool = False,
    skip: int = 0,
):
    logging.info(f"[STARTED] Fetching pull requests for {repo}")

    url = f"{settings.get_rest_base_uri()}/git/repositories/{repo}/pullrequests"
    params: dict[str, str | int] = {"$skip": skip}
    if not active_only:
        params["searchCriteria.status"] = "all"

    response = requests.get(
        url,
        params=params,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        logging.info(f"[COMPLETED] Fetching pull requests for {repo}")
        return [
            PullRequest.from_data(
                repo=repo, data=pr, discard_name_str=settings.get_name_discard_str()
            )
            for pr in response.json()["value"]
        ]

    logging.error(f"Error fetching pull requests for {repo}: {response.text}")
    raise ValueError("Cannot fetch data")


def fetch(settings: Azdo_Settings, repo: str, active_only: bool = False):
    logging.info(f"[STARTED] Fetching pull requests for {repo}")

    prs = data_cache.get(f"Pull Request {repo}")
    if prs:
        logging.info(f"Found pull requests for {repo} in cache")
        return prs

    prs = []
    results = fetch_pull_requests(settings=settings, repo=repo, active_only=active_only)

    while results:
        prs += results
        results = fetch_pull_requests(
            settings=settings, repo=repo, active_only=active_only, skip=len(prs)
        )

    logging.info(f"Cache pull requests for {repo}.")
    data_cache.push(key=f"Pull Request {repo}", value=prs)

    logging.info(f"[COMPLETED] Fetching pull requests for {repo}")
    return prs
