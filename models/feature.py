from typing import Any

from models.work_item import WorkItem


class Feature(WorkItem):
    kind: str = "Feature"

    @classmethod
    def from_data(cls, data: dict[str, Any], discard_name_str: list[str]) -> "Feature":
        """Create a Feature object from a dict of data.

        :param data: dict of data
        :param discard_name_str: list of strings to discard from the name
        :return: Feature object
        """
        return Feature(
            **WorkItem.from_data(
                data=data, discard_name_str=discard_name_str
            ).model_dump()
        )
