from datetime import datetime
from typing import Any

from pydantic import BaseModel

from utils.date_utils import to_date


class PipelineRun(BaseModel):
    id: str
    name: str
    state: str
    result: str | None
    created_date: datetime | None
    finished_date: datetime | None = None
    run_duration: float | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "PipelineRun":
        created_date = to_date(date_str=data.get("createdDate"))
        finished_date = to_date(date_str=data.get("finishedDate"))

        run_duration = (
            (finished_date - created_date).total_seconds()
            if created_date and finished_date
            else None
        )

        return PipelineRun(
            id=str(data["id"]),
            name=data["name"],
            state=data["state"],
            result=data.get("result"),
            created_date=created_date,
            finished_date=finished_date,
            run_duration=run_duration,
        )


class Pipeline(BaseModel):
    id: str
    name: str
    runs: list[PipelineRun] = []

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Pipeline":
        return Pipeline(
            id=str(data["id"]),
            name=data["name"],
        )
