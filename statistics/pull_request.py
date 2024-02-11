from collections import defaultdict

from pydantic import BaseModel

from models.git_commit import GitCommit
from models.pull_request import PullRequest
from services.git_commits import fetch as fetch_commits
from services.git_repositories import fetch as fetch_repositories
from services.pull_requests import fetch as fetch_pull_requests
from utils.display import Table, as_table_group, plot_bar_chart


class CountItem(BaseModel):
    total: int = 0
    active: int = 0
    completed: int = 0
    abandoned: int = 0
    reviewed: int = 0


class GitCommitCountItem(BaseModel):
    total: int = 0
    added: int = 0
    deleted: int = 0
    edited: int = 0


def aggr_commits(results: list[GitCommit]) -> list[tuple[str, int, int, int, int]]:
    """Aggregate commits by engineer.

    :param results: The list of commits.
    :return: The aggregated commits.
    """
    engineers = set([result.committer for result in results])
    counts: dict[str, GitCommitCountItem] = {
        engr: GitCommitCountItem() for engr in engineers
    }

    for engr in engineers:
        for commit in filter(lambda x: x.committer == engr, results):
            counts[engr].total += commit.added + commit.deleted + commit.edited
            counts[engr].added += commit.added
            counts[engr].deleted += commit.deleted
            counts[engr].edited += commit.edited

    response = [(k, v.total, v.added, v.deleted, v.edited) for k, v in counts.items()]
    response.sort(key=lambda x: x[1], reverse=True)
    return response


def aggr(results: list[PullRequest]) -> list[tuple[str, int, int, int, int, int]]:
    """Aggregate pull requests by engineer.

    :param results: The list of pull requests.
    :return: The aggregated pull requests.
    """
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
    """Calculate the time to merge.

    :param repo: The repository name.
    :param results: The list of pull requests.
    :return: The time to merge.
    """
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


def by_week(title: str, results: list[PullRequest]) -> Table:
    """Returns pull requests by week.

    :param title: The title of the table.
    :param results: The list of pull requests.
    :return: Display table object.
    """
    weeks = set([r.created_week for r in results])
    for result in results:
        if result.closed_week:
            weeks.add(result.closed_week)
    weeks = weeks = sorted(list(weeks))

    data = [
        (
            week,
            len([r for r in results if r.created_week == week]),
            len([r for r in results if r.closed_week == week]),
        )
        for week in weeks
    ]

    return Table(
        title=title,
        headers=["week", "created", "closed"],
        data=data,
        streamlit_chart=lambda df: plot_bar_chart(
            df=df, x_column="week", value_vars=["created", "closed"]
        ),
    )


def tbl(title: str, data: list[tuple[str, int, int, int, int, int]]) -> Table:
    """Returns pull requests table.

    :param title: The title of the table.
    :param data: The data to be aggregated.
    :return: Display table object.
    """
    return Table(
        title=title,
        headers=["engineer", "created", "active", "completed", "abandoned", "reviewed"],
        data=data,
    )


def tbl_commits(title: str, data: list[tuple[str, int, int, int, int]]) -> Table:
    """Returns git commits table.

    :param title: The title of the table.
    :param data: The data to be aggregated.
    :return: Display table object.
    """
    return Table(
        title=title,
        headers=["engineer", "total", "files added", "files deleted", "files edited"],
        data=data,
    )


def generate(title: str, streamlit: bool = False):
    """Generate statistics for pull requests.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    repos = fetch_repositories()
    total_prs = []
    total_commits = []
    merge_times = []

    tables = []

    for repo in repos:
        prs = fetch_pull_requests(repo)
        commits = fetch_commits(repo)

        tables.append(tbl(title=repo, data=aggr(prs)))
        tables.append(by_week(title=f"{repo} (by week)", results=prs))
        tables.append(tbl_commits(title=f"{repo} commits", data=aggr_commits(commits)))
        merge_times.append(time_to_merge(repo, prs))

        total_commits += commits
        total_prs += prs

    if len(repos) > 1:
        tables.append(tbl(title="total", data=aggr(total_prs)))

    tables.append(
        Table(
            title="days to merge",
            headers=["repo", "mean", "median", "max", "min"],
            data=merge_times,
        )
    )

    as_table_group(group_name=title, tables=tables, tabs=True, streamlit=streamlit)
