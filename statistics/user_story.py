from tabulate import tabulate

import services.user_stories as us_svc
import utils.aggr_utils as aggr_utils
from configurations.azdo_settings import Azdo_Settings
from models.user_story import UserStory


def aggr_accumulated(user_stories: list[UserStory]):
    aggr_created = aggr_utils.aggr_count(
        user_stories, "created_week", sort_values=False
    )
    aggr_closed = aggr_utils.aggr_count(user_stories, "closed_week", sort_values=False)
    aggr_removed = aggr_utils.aggr_count(
        [x for x in user_stories if x.state == "Removed"],
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

    return results


def generate():
    settings = Azdo_Settings.model_validate({})
    user_stories = us_svc.get_user_stories(settings)

    print("User Stories by states")
    print(
        tabulate(
            tabular_data=aggr_utils.aggr_count(data=user_stories, dimension="state"),
            headers=["state", "count"],
            tablefmt="fancy_grid",
        )
    )

    created_by = aggr_utils.aggr_count(data=user_stories, dimension="created_by")
    assigned = aggr_utils.aggr_count(data=user_stories, dimension="assigned_to")
    closed_by = aggr_utils.aggr_count(data=user_stories, dimension="closed_by")
    removed_by = aggr_utils.aggr_count(
        [us for us in user_stories if us.state == "Removed"], "changed_by"
    )
    merged = aggr_utils.merge([created_by, assigned, closed_by, removed_by])
    merged.sort(key=lambda x: x[1], reverse=True)

    print("Contributors to user stories")
    print(
        tabulate(
            tabular_data=merged,
            headers=["engineer", "created", "assigned", "closed", "removed"],
            tablefmt="fancy_grid",
        )
    )

    print("Accumulated User Stories")
    print(
        tabulate(
            tabular_data=aggr_accumulated(user_stories),
            headers=["week", "# created", "# closed", "# removed", "accumulated"],
            tablefmt="fancy_grid",
        )
    )

    print("User Stories by story points")
    print(
        tabulate(
            tabular_data=aggr_utils.aggr_count(user_stories, "story_points"),
            headers=["points", "count"],
            tablefmt="fancy_grid",
        )
    )


generate()
