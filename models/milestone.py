import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from utils.date_utils import to_date


class Milestone(BaseModel):
    name: str
    path: str
    timeframe: str
    start_date: datetime | None
    finish_date: datetime | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Milestone":
        """Create a Milestone object from a dict of data.

        :param data: dict of data
        :return: Milestone object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating Milestone from data")

        result = Milestone(
            name=data["name"],
            path=data["path"],
            timeframe=data["attributes"].get("timeFrame"),
            start_date=to_date(data["attributes"].get("startDate")),
            finish_date=to_date(
                data["attributes"].get("finishDate"),
            ),
        )

        logger.debug("[END] Creating Milestone from data")
        return result
