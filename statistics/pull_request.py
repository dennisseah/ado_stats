from collections import defaultdict

from pydantic import BaseModel
from tabulate import tabulate

import services.pull_requests as pr_svc
from configurations.azdo_settings import Azdo_Settings
from models.pull_request import PullRequest


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

    return [
        (k, v.total, v.active, v.completed, v.abandoned, v.reviewed)
        for k, v in counts.items()
    ]


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


def tbl(data: list[tuple[str, int, int, int, int, int]]):
    print(
        tabulate(
            tabular_data=data,
            headers=[
                "engineer",
                "created",
                "active",
                "completed",
                "abandoned",
                "reviewed",
            ],
            tablefmt="fancy_grid",
        )
    )


def generate():
    settings = Azdo_Settings.model_validate({})
    repos = pr_svc.get_all_repos(settings)
    total = []
    merge_times = []

    for repo in repos:
        prs = pr_svc.get_pull_requests(settings, repo)

        print(f"found {len(prs)} pull requests for {repo}")
        tbl(aggr(prs))
        merge_times.append(time_to_merge(repo, prs))
        total += prs

    print()
    print(f"found {len(total)} pull requests in total")
    tbl(aggr(total))

    print()
    print("days to merge pull requests")
    print(
        tabulate(
            tabular_data=merge_times,
            headers=["repo", "mean", "median", "max", "min"],
            tablefmt="fancy_grid",
        )
    )


generate()
