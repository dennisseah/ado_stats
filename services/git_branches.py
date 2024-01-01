import requests

from configurations.azdo_settings import Azdo_Settings
from models.git_branch import GitBranch
from utils.data_cache import DataCache

data_cache = DataCache()


def fetch(
    settings: Azdo_Settings,
    repo: str,
) -> list[GitBranch]:
    branches = data_cache.get("Git Branches")
    if branches:
        return branches

    url = f"{settings.get_rest_base_uri()}/git/repositories/{repo}/refs"
    params: dict[str, str | int] = {
        "api-version": "7.0",
        "$top": 200,
        "filter": "heads/",
    }

    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        branches = [
            GitBranch.from_data(
                repo=repo, data=d, discard_name_str=settings.get_name_discard_str()
            )
            for d in response.json()["value"]
        ]
        data_cache.push(key="Git Branches", value=branches)
        return branches
    else:
        raise ValueError("Cannot fetch data")
