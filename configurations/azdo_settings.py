from pydantic_settings import BaseSettings


class Azdo_Settings(BaseSettings):
    azdo_org_name: str
    azdo_project_name: str
    azdo_pat: str
    repos_ignore: str | None = None
