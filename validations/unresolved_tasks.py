from configurations.azdo_settings import Azdo_Settings
from models.user_story import UserStory
from services.tasks import fetch as fetch_tasks
from services.workitems import fetch_work_items
from utils.display import Table, as_table


def validate(settings: Azdo_Settings):
    tasks = fetch_tasks(settings)
    active_tasks = [
        t
        for t in tasks
        if t.parent_id is not None
        and t.state != "Closed"
        and t.state != "Resolved"
        and t.state != "Removed"
    ]
    parent_ids = list(set([t.parent_id for t in active_tasks]))
    user_stories = fetch_work_items(
        settings=settings, item_ids=parent_ids, creator=UserStory.from_data
    )
    closed_stories = [
        (us.id, us.created_by)
        for us in user_stories
        if us.state == "Closed" or us.state == "Removed" or us.state == "Resolved"
    ]

    results = []
    for us in closed_stories:
        unresolved_tasks = [t for t in active_tasks if t.parent_id == us[0]]
        for task in unresolved_tasks:
            results.append((task.id, task.assigned_to, us[0], us[1]))

    as_table(
        Table(
            title="Unresolved tasks",
            headers=["task id", "assigned to", "user story", "creator"],
            data=results,
        )
    )


settings = Azdo_Settings.model_validate({})
validate(settings)
