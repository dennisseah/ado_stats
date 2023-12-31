from typing import Any

from models.work_item import WorkItem


class Feature(WorkItem):
    kind: str = "Feature"

    @classmethod
    def from_data(cls, data: dict[str, Any], discard_name_str: list[str]) -> "Feature":
        return Feature(
            **WorkItem.from_data(
                data=data, discard_name_str=discard_name_str
            ).model_dump()
        )
