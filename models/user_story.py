from typing import Any

from models.work_item import WorkItem


class UserStory(WorkItem):
    kind: str = "User Story"

    @classmethod
    def from_data(
        cls, data: dict[str, Any], discard_name_str: list[str]
    ) -> "UserStory":
        return UserStory(
            **WorkItem.from_data(data, discard_name_str=discard_name_str).model_dump()
        )
