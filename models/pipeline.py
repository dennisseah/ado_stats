import logging
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
        """Create a PipelineRun object from a dict of data.

        :param data: dict of data
        :return: PipelineRun object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating PipelineRun from data")

        created_date = to_date(date_str=data.get("createdDate"))
        finished_date = to_date(date_str=data.get("finishedDate"))

        run_duration = (
            (finished_date - created_date).total_seconds()
            if created_date and finished_date
            else None
        )

        result = PipelineRun(
            id=str(data["id"]),
            name=data["name"],
            state=data["state"],
            result=data.get("result"),
            created_date=created_date,
            finished_date=finished_date,
            run_duration=run_duration,
        )

        logger.debug("[END] Creating PipelineRun from data")
        return result


class Pipeline(BaseModel):
    id: str
    name: str
    runs: list[PipelineRun] = []

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Pipeline":
        """Create a Pipeline object from a dict of data.

        :param data: dict of data
        :return: Pipeline object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating Pipeline from data")

        result = Pipeline(
            id=str(data["id"]),
            name=data["name"],
        )

        logger.debug("[END] Creating Pipeline from data")
        return result
