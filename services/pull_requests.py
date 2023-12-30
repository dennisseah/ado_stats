import requests

from configurations.azdo_settings import Azdo_Settings
from models.pull_request import PullRequest


def fetch_pull_requests(
    settings: Azdo_Settings,
    repo: str,
    active_only: bool = False,
    skip: int = 0,
):
    url = f"{settings.get_rest_base_uri()}/repositories/{repo}/pullrequests"
    params: dict[str, str | int] = {"$skip": skip}
    if not active_only:
        params["searchCriteria.status"] = "all"

    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        return [PullRequest.from_json(repo, pr) for pr in response.json()["value"]]

    raise ValueError("Cannot fetch data")


def get_pull_requests(settings: Azdo_Settings, repo: str, active_only: bool = False):
    prs = []
    results = fetch_pull_requests(settings=settings, repo=repo, active_only=active_only)

    while results:
        prs += results
        results = fetch_pull_requests(
            settings=settings, repo=repo, active_only=active_only, skip=len(prs)
        )

    return prs


def get_all_repos(settings: Azdo_Settings):
    url = f"{settings.get_rest_base_uri()}/repositories"
    response = requests.get(url, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        repos = [repo["name"] for repo in response.json()["value"]]
        ignores = settings.get_ignored_repos()

        if ignores:
            repos = [repo for repo in repos if repo not in ignores]

        return repos

    raise ValueError("Cannot fetch git repositories")
