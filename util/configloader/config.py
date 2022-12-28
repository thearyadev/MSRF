import dataclasses

import yaml
from types import SimpleNamespace
import util
from pydantic import BaseModel


class Config(BaseModel):
    pc_user_agent: str | None
    mobile_user_agent: str | None
    database_url: str | None
    LANG: str | None
    GEO: str | None
    TZ: str | None
    debug: bool


def load_config(file: str) -> Config:
    with open(file, "r") as f:
        return Config(**yaml.safe_load(f))


if __name__ == '__main__':
    print(load_config("../../configuration.yaml"))