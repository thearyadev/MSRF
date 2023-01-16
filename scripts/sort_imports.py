import isort
import glob
from rich.progress import track
import subprocess


def exec_file(file: str):
    if "__init__" not in file:  # do not run in __init__.py files
        print(f"running on file: {file}")
        subprocess.run(
            f"autoflake --in-place --remove-unused-variables --remove-all-unused-imports  {file}")
        isort.file(file)


if __name__ == '__main__':
    dirs = ["custom_logging", "database", "util", "tests", "gui", "error_reporting", "update"]
    files = ["main.py", ]

    for d in track(dirs, "running"):
        gb = glob.glob(f"{d}/**/*.py", recursive=True)
        gb.extend(files)
        for f in gb:
            exec_file(f)
