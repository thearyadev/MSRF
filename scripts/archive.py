import logging
import shutil
from types import SimpleNamespace

import yaml

if __name__ == "__main__":
    with open("configuration.yaml", "r") as file:
        config = SimpleNamespace(**yaml.safe_load(file))
    shutil.make_archive(
        f"./deployable/msrf-windows-64_{config.version}", "zip", "./dist"
    )
