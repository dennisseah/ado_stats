import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from models.pull_request import PullRequest
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch_pull_requests(
    repo: str,
    active_only: bool = False,
    skip: int = 0,
):
    """Fetch pull requests for a repo.

    :param repo: The repo name.
    :param active_only: If True, only active pull requests will be returned.
    :param skip: The number of pull requests to skip.
    :return: A list of PullRequest objects.
    """
    settings = Azdo_Settings.model_validate({})
    logger = logging.getLogger(__name__)
    logger.debug(f"[BEGIN] Fetching pull requests for {repo}")

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
        logger.debug(f"[END] Fetching pull requests for {repo}")
        return [
            PullRequest.from_data(
                repo=repo, data=pr, discard_name_str=settings.get_name_discard_str()
            )
            for pr in response.json()["value"]
        ]

    logger.error(f"Error fetching pull requests for {repo}: {response.text}")
    raise ValueError("Cannot fetch data")


def fetch(repo: str, active_only: bool = False) -> list[PullRequest]:
    """Fetch pull requests for a repo.

    :param repo: The repo name.
    :param active_only: If True, only active pull requests will be returned.
    :return: A list of PullRequest objects.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"[BEGIN] Fetching pull requests for {repo}")

    prs = data_cache.get(f"Pull Request {repo}")
    if prs:
        logger.debug(f"Found pull requests for {repo} in cache")
        return prs

    prs = []
    results = fetch_pull_requests(repo=repo, active_only=active_only)

    while results:
        prs += results
        results = fetch_pull_requests(repo=repo, active_only=active_only, skip=len(prs))

    logger.debug(f"Cache pull requests for {repo}.")
    data_cache.push(key=f"Pull Request {repo}", value=prs)

    logger.debug(f"[END] Fetching pull requests for {repo}")
    return prs
