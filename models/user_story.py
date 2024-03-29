import logging
from typing import Any

from models.work_item import WorkItem


class UserStory(WorkItem):
    kind: str = "User Story"

    @classmethod
    def from_data(
        cls, data: dict[str, Any], discard_name_str: list[str]
    ) -> "UserStory":
        """Create a UserStory object from a dict of data.

        :param data: dict of data
        :param discard_name_str: list of strings to discard from the name
        :return: UserStory object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating UserStory from data")

        result = UserStory(
            **WorkItem.from_data(data, discard_name_str=discard_name_str).model_dump()
        )

        logger.debug("[END] Creating UserStory from data")
        return result

    def is_completed(self) -> bool:
        """Check if the user story is completed.

        :return: True if completed, False otherwise
        """
        return self.state in ["Closed", "Resolved", "Done", "Removed"]
