from configurations.azdo_settings import Azdo_Settings
from services.tasks import fetch as fetch_tasks
from utils.display import Table, as_table


def validate(settings: Azdo_Settings):
    tasks = fetch_tasks(settings)
    orphaned_tasks = [
        t
        for t in tasks
        if t.parent_id is None and t.state != "Closed" and t.state != "Removed"
    ]
    as_table(
        Table(
            title="Orphan tasks",
            headers=["task id", "assigned to"],
            data=[(t.id, t.assigned_to) for t in orphaned_tasks],
        )
    )


settings = Azdo_Settings.model_validate({})
validate(settings)
