from models.work_item import WorkItem


class Task(WorkItem):
    kind: str = "Task"

    @classmethod
    def from_data(cls, data: dict) -> "Task":
        return Task(**WorkItem.from_data(data).model_dump())
