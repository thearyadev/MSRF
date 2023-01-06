import isort
import glob
from rich.progress import track
import subprocess


def exec_file(file: str):
    if "__init__" not in file:
        subprocess.run(
            f"autoflake --in-place --remove-unused-variables --remove-all-unused-imports  {file}")
        isort.file(file)


if __name__ == '__main__':
    dirs = ["custom_logging", "database", "util", "tests"]
    files = ["main.py", ]

    for d in track(dirs, "stage 1"):
        gb = glob.glob(f"{d}/**/*.py", recursive=True)
        for f in gb:
            exec_file(f)

    for f in track(files, "stage 2"):
        exec_file(f)
