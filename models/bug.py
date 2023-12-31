from models.work_item import WorkItem


class Bug(WorkItem):
    kind: str = "Bug"

    @classmethod
    def from_data(cls, data: dict) -> "Bug":
        return Bug(**WorkItem.from_data(data).model_dump())
