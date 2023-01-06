import logging
import shutil

if __name__ == '__main__':
    shutil.make_archive("./dist/msrf-windows-64", "zip", "./dist")
