from models.work_item import WorkItem


class UserStory(WorkItem):
    @classmethod
    def from_data(cls, data: dict) -> "UserStory":
        return UserStory(**WorkItem.from_data(data).model_dump())
