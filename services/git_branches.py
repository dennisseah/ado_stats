import requests

from configurations.azdo_settings import Azdo_Settings
from models.git_branch import GitBranch


def fetch_git_branches(
    settings: Azdo_Settings,
    repo: str,
) -> list[GitBranch]:
    url = f"{settings.get_rest_base_uri()}/git/repositories/{repo}/refs"
    params: dict[str, str | int] = {
        "api-version": "7.0",
        "$top": 200,
        "filter": "heads/",
    }

    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        return [
            GitBranch.from_data(
                repo=repo, data=d, discard_name_str=settings.get_name_discard_str()
            )
            for d in response.json()["value"]
        ]
    else:
        raise ValueError("Cannot fetch data")
