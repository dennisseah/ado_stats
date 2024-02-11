import logging
from typing import Any

from pydantic import BaseModel

import utils.date_utils as date_utils


class GitCommit(BaseModel):
    repo: str
    committer: str
    comments: str
    added: int = 0
    deleted: int = 0
    edited: int = 0
    commit_date: str = ""

    @classmethod
    def from_data(cls, repo: str, data: dict[str, Any]) -> "GitCommit":
        """Create a GitCommit object from a dict of data.

        :param repo: name of the repo
        :param data: dict of data
        :return: GitCommit object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating GitCommit from data")

        result = GitCommit(
            repo=repo,
            committer=data["committer"]["name"],
            comments=data["comment"],
            added=data["changeCounts"]["Add"],
            deleted=data["changeCounts"]["Delete"],
            edited=data["changeCounts"]["Edit"],
            commit_date=date_utils.to_date_str(
                date_utils.to_date(data["committer"]["date"])
            ),
        )

        logger.debug("[END] Creating GitCommit from data")
        return result
