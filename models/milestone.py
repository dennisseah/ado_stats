from datetime import datetime
from typing import Any

from pydantic import BaseModel

from utils.date_utils import to_date


class Milestone(BaseModel):
    name: str
    path: str
    start_date: datetime | None
    finish_date: datetime | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Milestone":
        return Milestone(
            name=data["name"],
            path=data["path"],
            start_date=to_date(data["attributes"].get("startDate")),
            finish_date=to_date(
                data["attributes"].get("finishDate"),
            ),
        )
