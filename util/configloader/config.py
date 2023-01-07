import yaml
from pydantic import BaseModel


class Config(BaseModel):
    pc_user_agent: str | None
    mobile_user_agent: str | None
    LANG: str | None
    GEO: str | None
    TZ: str | None
    debug: bool | None
    minimum_auto_rerun_delay_seconds: int | None
    gui_window_opacity: float | None
    hydration_rate: int | None
    max_account_number: int | None
    version: str | None
    program_name: str | None
    product_name: str | None


def load_config(file: str) -> Config:
    with open(file, "r") as f:
        return Config(**yaml.safe_load(f))


if __name__ == '__main__':
    print(load_config("../../configuration.yaml"))
