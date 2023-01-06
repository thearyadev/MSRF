from github import Github
from pydantic import BaseModel


class VersionInfo(BaseModel):
    release_url: str
    release_version: str


def check_version() -> VersionInfo:
    try:
        d = Github().get_repo("thearyadev/MSRF").get_latest_release()
        return VersionInfo(release_url=d.html_url, release_version=d.tag_name)
    except Exception as e:
        return VersionInfo(release_url="", release_version="")
