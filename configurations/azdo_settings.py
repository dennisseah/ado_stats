import urllib.parse as parser

from pydantic_settings import BaseSettings


class Azdo_Settings(BaseSettings):
    azdo_org_name: str
    azdo_project_name: str
    azdo_pat: str
    area_paths: str | None = None
    repos_ignore: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

    def get_area_paths(self) -> list[str]:
        return (
            [r.strip() for r in self.area_paths.split(",")] if self.area_paths else []
        )

    def get_ignored_repos(self) -> list[str]:
        return (
            [r.strip() for r in self.repos_ignore.split(",")]
            if self.repos_ignore
            else []
        )

    def get_rest_base_uri(self) -> str:
        return f"https://dev.azure.com/{self.azdo_project_name}/{parser.quote(self.azdo_org_name)}/_apis"
