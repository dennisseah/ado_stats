import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from utils.date_utils import to_date, to_week
from utils.name_formatter import format_name


class PullRequest(BaseModel):
    repo: str
    status: str
    is_draft: bool
    merge_days: int | None
    created_by: str
    created_date: datetime
    created_week: str
    closed_date: datetime | None = None
    closed_week: str | None = None
    reviewers: list[str] = []

    @classmethod
    def from_data(
        cls, repo: str, data: dict[str, Any], discard_name_str: list[str]
    ) -> "PullRequest":
        """Create a PullRequest object from a dict of data.

        :param repo: name of the repo
        :param data: dict of data
        :param discard_name_str: list of strings to discard from the name
        :return: PullRequest object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating PullRequest from data")

        created_by = format_name(
            name=data["createdBy"]["displayName"],
            discard_str=discard_name_str,
        )
        d_create = to_date(data["creationDate"])
        created_week = to_week(d_create)

        d_close = to_date(data.get("closedDate"))
        closed_week = to_week(d_close) if d_close else None

        # created_date will never be None
        merge_days = (d_close - d_create).days if d_close else None  # type: ignore

        reviewers = [
            format_name(name=r["displayName"], discard_str=discard_name_str)
            for r in data.get("reviewers", [])
            if r.get("vote", 0) > 0
        ]

        result = PullRequest(
            repo=repo,
            status=data["status"],
            is_draft=data.get("isDraft", False),
            merge_days=merge_days,
            created_by=created_by,
            created_date=d_create,  # type: ignore
            created_week=created_week,  # type: ignore
            closed_date=d_close,
            closed_week=closed_week,
            reviewers=reviewers,
        )

        logger.debug("[END] Creating PullRequest from data")
        return result
