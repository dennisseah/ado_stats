from collections import defaultdict

from pydantic import BaseModel

from configurations.azdo_settings import Azdo_Settings
from models.pull_request import PullRequest
from services.git_repositories import fetch as fetch_repositories
from services.pull_requests import fetch as fetch_pull_requests
from utils.display import Table, as_table_group


class CountItem(BaseModel):
    total: int = 0
    active: int = 0
    completed: int = 0
    abandoned: int = 0
    reviewed: int = 0


def aggr(results: list[PullRequest]) -> list[tuple[str, int, int, int, int, int]]:
    engineers = set([result.created_by for result in results])
    counts: dict[str, CountItem] = {}

    for engr in engineers:
        counts[engr] = CountItem(
            total=len([x for x in results if x.created_by == engr]),
            active=len(
                [x for x in results if x.created_by == engr and x.status == "active"]
            ),
            completed=len(
                [x for x in results if x.created_by == engr and x.status == "completed"]
            ),
            abandoned=len(
                [x for x in results if x.created_by == engr and x.status == "abandoned"]
            ),
        )

    reviewers = defaultdict(int)
    for pr in results:
        for reviewer in pr.reviewers:
            reviewers[reviewer] += 1

    for engr in engineers:
        counts[engr].reviewed = reviewers.get(engr, 0)

    for engr in filter(lambda x: x not in engineers, reviewers.keys()):
        counts[engr] = CountItem(reviewed=reviewers[engr])

    response = [
        (k, v.total, v.active, v.completed, v.abandoned, v.reviewed)
        for k, v in counts.items()
    ]
    response.sort(key=lambda x: x[1], reverse=True)

    return response


def time_to_merge(
    repo: str, results: list[PullRequest]
) -> tuple[str, int, int, int, int]:
    data = [r.merge_days for r in results if r.merge_days is not None]

    return (
        (
            repo,
            round(sum(data) / len(data)),
            data[round(len(data) / 2)],
            max(data),
            min(data),
        )
        if data
        else (repo, 0, 0, 0, 0)
    )


def tbl(title: str, data: list[tuple[str, int, int, int, int, int]]) -> Table:
    return Table(
        title=title,
        headers=[
            "engineer",
            "created",
            "active",
            "completed",
            "abandoned",
            "reviewed",
        ],
        data=data,
    )


def generate(settings: Azdo_Settings, title: str, streamlit: bool = False):
    settings = Azdo_Settings.model_validate({})
    repos = fetch_repositories(settings)
    total = []
    merge_times = []

    tables = []

    for repo in repos:
        prs = fetch_pull_requests(settings, repo)
        tables.append(tbl(title=repo, data=aggr(prs)))
        merge_times.append(time_to_merge(repo, prs))
        total += prs

    if len(repos) > 1:
        tables.append(tbl(title="total", data=aggr(total)))

    tables.append(
        Table(
            title="days to merge",
            headers=["repo", "mean", "median", "max", "min"],
            data=merge_times,
        )
    )

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
