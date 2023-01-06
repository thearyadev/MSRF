import os
import shutil
import pathlib
import yaml
from types import SimpleNamespace
import sys

"""This script will build the executable and package directory for msrf. Attributes are taken from configuration.yaml"""


def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


if __name__ == '__main__':
    if get_base_prefix_compat() == sys.prefix:
        print("Run this script in a Python virtual environment.")

    files_to_copy = [
        pathlib.Path("./configuration.yaml"),
        pathlib.Path("./LICENSE"),
        pathlib.Path("./README.md")
    ]

    directories_to_copy = [
        pathlib.Path("./bin")
    ]
    target_directory: pathlib.Path = pathlib.Path("./dist")
    build_dir: pathlib.Path = pathlib.Path("./build")
    with open("configuration.yaml", "r") as file:
        config = SimpleNamespace(**yaml.safe_load(file))

    try:
        shutil.rmtree(target_directory)
    except FileNotFoundError:
        pass

    try:
        os.mkdir(target_directory)
    except FileExistsError:
        pass
    flet_pack = 'flet pack main.py ' \
                f'--name "{config.program_name}" ' \
                f'--product-name "{config.product_name}" ' \
                f'--product-version "{config.version}" ' \
                f'--file-description "{config.product_name}" ' \
                '--icon "assets/msrf.ico"'
    os.system(flet_pack)
    for directory in directories_to_copy:
        subdir = pathlib.Path(f"{target_directory.name}/{directory.name}")
        shutil.copytree(directory, subdir)

    for file in files_to_copy:
        target_file = pathlib.Path(f"{target_directory.name}/{file.name}")
        shutil.copy(file, target_file)

    try:
        shutil.rmtree(build_dir)
    except FileNotFoundError:
        pass
