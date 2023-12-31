from typing import Any

from tabulate import tabulate

from utils.aggr_utils import aggr_count, merge


def aggr_state(data: list[Any]):
    print(
        tabulate(
            tabular_data=aggr_count(data=data, dimension="state"),
            headers=["state", "count"],
            tablefmt="fancy_grid",
        )
    )


def aggr_accumulated(data: list[Any]):
    aggr_created = aggr_count(data, "created_week", sort_values=False)
    aggr_closed = aggr_count(data, "closed_week", sort_values=False)
    aggr_removed = aggr_count(
        [x for x in data if x.state == "Removed"],
        "changed_week",
        sort_values=False,
    )

    removed = {x[0]: x[1] for x in aggr_removed}
    closed = {x[0]: x[1] for x in aggr_closed}

    created_weeks = [x[0] for x in aggr_created]
    for x in removed.keys():
        if x not in created_weeks:
            aggr_created.append((x, 0))
    for x in closed.keys():
        if x not in created_weeks:
            aggr_created.append((x, 0))
    aggr_created.sort(key=lambda x: x[0])

    results = []
    accumulated = 0

    for created in aggr_created:
        accumulated += (
            created[1] - closed.get(created[0], 0) - removed.get(created[0], 0)
        )
        results.append(
            (
                created[0],
                created[1],
                closed.get(created[0], 0),
                removed.get(created[0], 0),
                accumulated,
            )
        )

    print(
        tabulate(
            tabular_data=results,
            headers=[
                "year - week",
                "# created",
                "# closed",
                "# removed",
                "accumulated",
            ],
            tablefmt="fancy_grid",
        )
    )


def lifecycle(data: list[Any]):
    created_by = aggr_count(data=data, dimension="created_by")
    assigned = aggr_count(data=data, dimension="assigned_to")
    closed_by = aggr_count(data=data, dimension="closed_by")
    removed_by = aggr_count([us for us in data if us.state == "Removed"], "changed_by")
    merged = merge([created_by, assigned, closed_by, removed_by])
    merged.sort(key=lambda x: x[1], reverse=True)

    print(
        tabulate(
            tabular_data=merged,
            headers=["engineer", "created", "assigned", "closed", "removed"],
            tablefmt="fancy_grid",
        )
    )
