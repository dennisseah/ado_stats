from services.tasks import fetch as fetch_tasks
from utils.display import Table, as_table


def validate():
    tasks = fetch_tasks()
    orphaned_tasks = [
        t
        for t in tasks
        if t.parent_id is None
        and t.state != "Closed"
        and t.state != "Resolved"
        and t.state != "Removed"
    ]
    as_table(
        Table(
            title="Orphan tasks",
            headers=["task id", "assigned to"],
            data=[(t.id, t.assigned_to) for t in orphaned_tasks],
        )
    )


if __name__ == "__main__":
    validate()
