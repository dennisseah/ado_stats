from configurations.azdo_settings import Azdo_Settings
from models.git_branch import GitBranch
from services.git_branches import fetch as fetch_branches
from services.git_repositories import fetch as fetch_repositories
from utils.display import Table, as_table_group


def generate(settings: Azdo_Settings):
    repos = fetch_repositories(settings=settings)

    branches: list[GitBranch] = []

    for repo in repos:
        branches += fetch_branches(settings=settings, repo=repo)

    data = [
        (br.repo, br.name, br.creator)
        for br in branches
        if br.name != "main" and br.name != "master"
    ]
    data.sort(key=lambda x: x[0])

    as_table_group(
        group_name="Git branches",
        tables=[
            Table(title="Git branches", headers=["repo", "name", "creator"], data=data)
        ],
    )
