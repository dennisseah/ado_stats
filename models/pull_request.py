from datetime import datetime
from typing import Any

from pydantic import BaseModel

from utils.date_utils import to_date


class PullRequest(BaseModel):
    repo: str
    status: str
    is_draft: bool
    merge_days: int | None
    created_by: str
    created_date: datetime
    closed_date: datetime | None = None
    reviewers: list[str] = []

    @classmethod
    def from_json(cls, repo: str, data: dict[str, Any]) -> "PullRequest":
        created_by = (
            data["createdBy"]["displayName"]
            .replace("(Contractor)", "")
            .replace("Microsoft", "")
            .strip()
        )
        d_create = to_date(data["creationDate"])
        d_close = to_date(data.get("closedDate"))

        # created_date will never be None
        merge_days = (d_close - d_create).days if d_close else None  # type: ignore

        reviewers = [
            r["displayName"] for r in data.get("reviewers", []) if r.get("vote", 0) > 0
        ]
        return PullRequest(
            repo=repo,
            status=data["status"],
            is_draft=data.get("isDraft", False),
            merge_days=merge_days,
            created_by=created_by,
            created_date=d_create,  # type: ignore
            closed_date=d_close,
            reviewers=reviewers,
        )
