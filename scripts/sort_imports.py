import isort
import glob
from rich.progress import track

if __name__ == '__main__':
    dirs = ["custom_logging", "database", "util", "tests"]
    files = ["main.py", ]

    for d in track(dirs, "stage 1"):
        gb = glob.glob(f"{d}/**/*.py", recursive=True)
        for f in gb:
            isort.file(f)

    for f in track(files, "stage 2"):
        isort.file(f)
