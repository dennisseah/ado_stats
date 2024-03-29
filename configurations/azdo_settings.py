import urllib.parse as parser

from pydantic_settings import BaseSettings, SettingsConfigDict


class Azdo_Settings(BaseSettings):
    """Azure DevOps settings"""

    azdo_org_name: str
    azdo_project_name: str
    azdo_pat: str
    area_paths: str | None = None
    repos_ignore: str | None = None
    name_discard_str: str | None = None
    crew: str | None = None
    pull_requests_name_aliases: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    def get_area_paths(self) -> list[str]:
        """Area paths are comma separated values. This method returns a list of area
           paths.

        Area paths are how Azure DevOps organizes work items.
        """
        return (
            [r.strip() for r in self.area_paths.split(",")] if self.area_paths else []
        )

    def get_name_discard_str(self) -> list[str]:
        """Name discard strings are comma separated values. This method returns a list
        of name discard strings.

        Names in the Azure DevOps work items are maybe suffixed with a label e.g.
        (Contractor)
        """
        return (
            [r.strip() for r in self.name_discard_str.split(",")]
            if self.name_discard_str
            else []
        )

    def get_ignored_repos(self) -> list[str]:
        """Ignored repos are comma separated values. This method returns a list of
        git repository names to ignore
        """
        return (
            [r.strip() for r in self.repos_ignore.split(",")]
            if self.repos_ignore
            else []
        )

    def get_rest_base_uri(self) -> str:
        return f"https://dev.azure.com/{self.azdo_project_name}/{parser.quote(self.azdo_org_name)}/_apis"

    def get_pull_requests_name_aliases(self) -> dict[str, str]:
        if not self.pull_requests_name_aliases:
            return {}

        aliases = {}
        for alias in self.pull_requests_name_aliases.split(";"):
            if alias:
                parts = alias.strip().split(":")
                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid alias format: {alias}. Must be in the format 'name:alias'"  # noqa E501
                    )
                aliases[parts[0]] = parts[1]

        return aliases
