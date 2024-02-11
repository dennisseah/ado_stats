import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from models.git_commit import GitCommit
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch_commits(repo: str, skip: int = 0):
    """Fetch git commits for a repo.

    :param repo: The repo name.
    :param skip: The number of git commits to skip.
    :return: A list of PullRequest objects.
    """
    settings = Azdo_Settings.model_validate({})
    logger = logging.getLogger(__name__)
    logger.debug(f"[BEGIN] Fetching git commits for {repo}")

    url = f"{settings.get_rest_base_uri()}/git/repositories/{repo}/commits"
    params: dict[str, str | int] = {
        "$skip": skip,
        "searchCriteria.itemVersion.version": "main",
    }

    response = requests.get(
        url,
        params=params,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        logger.debug(f"[END] Fetching git commits for {repo}")
        results = []

        for commit in response.json()["value"]:
            results.append(GitCommit.from_data(repo=repo, data=commit))
        return results

    logger.error(f"Error fetching git commits for {repo}: {response.text}")
    raise ValueError("Cannot fetch data")


def fetch(repo: str) -> list[GitCommit]:
    """Fetch git commits for a repo.

    :param repo: The repo name.
    :return: A list of GitCommits objects.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"[BEGIN] Fetching git commits for {repo}")

    commits = data_cache.get(f"Git Commit {repo}")
    if commits:
        logger.debug(f"Found git commits for {repo} in cache")
        return commits

    commits = []
    results = fetch_commits(repo=repo)

    while results:
        commits += results
        results = fetch_commits(repo=repo, skip=len(commits))

    logger.debug(f"Cache git commits for {repo}.")
    data_cache.push(key=f"Git Commit {repo}", value=commits)

    logger.debug(f"[END] Fetching git commits for {repo}")
    return commits
