import datetime
import threading
import time
import util
from types import SimpleNamespace
from rich import print
import database
import logging
import sys

from flask import Flask, render_template, redirect, Response


def configure_loggers():
    logging.basicConfig(
        format='%(name)s ---- [%(threadName)s] [%(asctime)s] [%(levelname)s]'
               ' [%(filename)s] [Line %(lineno)d] %(message)s',
        handlers=[
            logging.FileHandler("farmer.log"),
            logging.StreamHandler(),
        ],
        level=logging.DEBUG)
    logging.getLogger("werkzeug").setLevel(logging.CRITICAL)  # disable flask logger
    logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.CRITICAL)
    logging.getLogger("selenium.webdriver.common.selenium_manager").setLevel(logging.CRITICAL)
    logging.getLogger("selenium.webdriver.common.selenium_manager").setLevel(logging.CRITICAL)
    logging.getLogger("selenium.webdriver.common.service").setLevel(logging.CRITICAL)
    logging.getLogger("httpx._client").setLevel(logging.CRITICAL)


# Configure Logging
configure_loggers()


logger: logging.Logger = logging.getLogger("msrf")  # create msrf logger
config: SimpleNamespace = util.load_config("configuration.yaml")  # load config from file
logger.info("Loaded ./configuration.yaml into config SimpleNamespace")
db = database.DatabaseAccess(url=config.database_url)  # create database connection
logger.info(f"Connection to database ({config.database_url}) was successful.")

app = Flask(__name__, static_folder="./static", static_url_path="")  # init flask


@app.route("/")
def index():
    logger.info("Serving index webpage.")
    return render_template("index.html", accounts=db.read(), active_threads=[t.name for t in threading.enumerate()])


@app.route("/log")
def log():
    with open("farmer.log", "r") as file:
        return list(reversed(list(reversed(file.readlines()))[:15]))


@app.template_filter('strftime')
def _jinja2_filter_datetime(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


if __name__ == '__main__':
    for a in db.read():
        util.exec_farmer(a, config=config, db=db)
    app.run()

## PB PASSWORD C!ddKm9R5ESTJJz6
