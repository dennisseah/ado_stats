from tabulate import tabulate

from configurations.azdo_settings import Azdo_Settings
from models.git_branch import GitBranch
from services.git_branches import fetch_git_branches
from services.git_repositories import get_repos

settings = Azdo_Settings.model_validate({})
repos = get_repos(settings=settings)

branches: list[GitBranch] = []

for repo in repos:
    branches += fetch_git_branches(settings=settings, repo=repo)

data = [
    (br.repo, br.name, br.creator)
    for br in branches
    if br.name != "main" and br.name != "master"
]
data.sort(key=lambda x: x[0])
print("Git branches")
print(
    tabulate(
        tabular_data=data,
        headers=["repo", "name", "creator"],
        tablefmt="fancy_grid",
    )
)
