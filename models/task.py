import logging
from typing import Any

from models.work_item import WorkItem


class Task(WorkItem):
    kind: str = "Task"

    @classmethod
    def from_data(cls, data: dict[str, Any], discard_name_str: list[str]) -> "Task":
        """Create a Task object from a dict of data.

        :param data: dict of data
        :param discard_name_str: list of strings to discard from the name
        :return: Task object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating Task from data")

        result = Task(
            **WorkItem.from_data(
                data=data, discard_name_str=discard_name_str
            ).model_dump()
        )

        logger.debug("[END] Creating Task from data")
        return result
