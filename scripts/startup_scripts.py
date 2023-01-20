import subprocess


def flet_hot_reload_recursive_run():
    subprocess.run([
        "flet",
        "run",
        "main.py"
    ])


def flet_normal_python_start():
    subprocess.run([
        "python",
        "main.py"
    ])
