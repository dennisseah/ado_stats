import logging
from typing import Any

from models.work_item import WorkItem


class Bug(WorkItem):
    kind: str = "Bug"

    @classmethod
    def from_data(cls, data: dict[str, Any], discard_name_str: list[str]) -> "Bug":
        """Create a Bug object from a dict of data.

        :param data: dict of data
        :param discard_name_str: list of strings to discard from the name
        :return: Bug object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating Bug from data")
        result = Bug(
            **WorkItem.from_data(
                data=data, discard_name_str=discard_name_str
            ).model_dump()
        )
        logger.debug("[END] Creating Bug from data")
        return result
