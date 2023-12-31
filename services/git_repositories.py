import requests

from configurations.azdo_settings import Azdo_Settings


def fetch(settings: Azdo_Settings):
    url = f"{settings.get_rest_base_uri()}/git/repositories"
    response = requests.get(url, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        repos = [repo["name"] for repo in response.json()["value"]]
        ignores = settings.get_ignored_repos()

        if ignores:
            repos = [repo for repo in repos if repo not in ignores]

        return repos

    raise ValueError("Cannot fetch git repositories")
