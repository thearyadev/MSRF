import logging
import shutil

if __name__ == '__main__':
    shutil.make_archive("msrf-windows-64", "zip", "./dist")