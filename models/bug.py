from typing import Any

from models.work_item import WorkItem


class Bug(WorkItem):
    kind: str = "Bug"

    @classmethod
    def from_data(cls, data: dict[str, Any], discard_name_str: list[str]) -> "Bug":
        return Bug(
            **WorkItem.from_data(
                data=data, discard_name_str=discard_name_str
            ).model_dump()
        )
