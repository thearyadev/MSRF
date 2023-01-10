import yaml
from pydantic import BaseModel
from pydantic_yaml import YamlModel


class Config(YamlModel):
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
    theme_mode: str | None
    run_scheduler: bool | None

    @classmethod
    def load_config(cls, file: str):
        with open(file, "r") as f:
            return cls(**yaml.safe_load(f))

    def save_config(self, file: str):
        with open(file, "w") as f:
            f.write(self.yaml())


if __name__ == '__main__':
    a = Config.load_config("../../configuration.yaml")
    print(a)
    print(a.debug)
    a.debug = True
    a.save_config("../../configuration.yaml")
