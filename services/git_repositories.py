import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch() -> list[str]:
    """Fetch git repositories from Azure DevOps

    :return: A list of git repositories.
    """
    settings = Azdo_Settings.model_validate({})
    logging.info("[STARTED] Fetching git repositories")

    repos = data_cache.get("Git Repositories")
    if repos:
        logging.info("Found git repositories in cache")
        return repos

    url = f"{settings.get_rest_base_uri()}/git/repositories"
    response = requests.get(url, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        repos = [repo["name"] for repo in response.json()["value"]]
        ignores = settings.get_ignored_repos()

        if ignores:
            repos = [repo for repo in repos if repo not in ignores]

        logging.info("Cache git repositories.")
        data_cache.push(key="Git Repositories", value=repos)

        logging.info("[COMPLETED] Fetching git repositories")
        return repos

    logging.error(f"Error fetching git repositories: {response.text}")
    raise ValueError("Cannot fetch git repositories")
