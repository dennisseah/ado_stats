import logging
from typing import Any

from pydantic import BaseModel

from utils.name_formatter import format_name


class GitBranch(BaseModel):
    repo: str
    name: str
    creator: str

    @classmethod
    def from_data(
        cls, repo: str, data: dict[str, Any], discard_name_str: list[str]
    ) -> "GitBranch":
        """Create a GitBranch object from a dict of data.

        :param repo: name of the repo
        :param data: dict of data
        :param discard_name_str: list of strings to discard from the name
        :return: GitBranch object
        """
        logger = logging.getLogger(__name__)
        logger.debug("[BEGIN] Creating GitBranch from data")

        creator = format_name(
            name=data["creator"]["displayName"], discard_str=discard_name_str
        )
        result = GitBranch(
            repo=repo, name=data["name"].replace("refs/heads/", ""), creator=creator
        )

        logger.debug("[END] Creating GitBranch from data")
        return result
