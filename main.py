import datetime
import threading
import time
import util
from types import SimpleNamespace
from rich import print
import database
import logging
import sys
import atexit

from flask import Flask, render_template, redirect, Response
import schedule
from apscheduler.schedulers.background import BackgroundScheduler


def configure_loggers():
    logging.basicConfig(
        format='[%(threadName)s] [%(asctime)s] [%(levelname)s]'
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
config: util.Config = util.load_config("configuration.yaml")  # load config from file
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
        return list(reversed(list(reversed(file.readlines()))[:20]))


@app.route("/exec_single_account/<account_id>")
def exec_single_account(account_id: int):
    account: util.MicrosoftAccount = [a for a in db.read() if a.id == account_id][0]
    threading.Thread(
        name=account.email,
        target=util.exec_farmer,
        kwargs={"account": account, "config": config, "db": db}
    ).start()
    return redirect("/")


@app.template_filter('strftime')
def _jinja2_filter_datetime(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


def job():
    print("job run :D")


if __name__ == '__main__':
    #for a in db.read():
     #   util.exec_farmer(account=a,
      #                   config=config,
       #                  db=db)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=job, trigger="interval", hours=5)
    # scheduler.start()

    app.run(debug=config.debug)
# atexit.register(lambda: scheduler.shutdown())

## PB PASSWORD C!ddKm9R5ESTJJz6
