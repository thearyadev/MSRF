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
from apscheduler.schedulers.background import BackgroundScheduler
import flet as ft


def configure_loggers() -> list[None]:
    logging.basicConfig(
        format='%(name)s----[%(threadName)s] [%(asctime)s] [%(levelname)s]'
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
    logging.getLogger("root").disabled = True  # flet logger


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


def run_sequential_threads(accounts: list[util.MicrosoftAccount]):
    for account in accounts:  # loop over given accounts
        thread = threading.Thread(  # init thread object
            name=account.email,  # name of thread is the account email
            target=util.exec_farmer,
            kwargs={"account": account, "config": config, "db": db}
        )
        thread.start()  # start thread
        # wait for 3600 seconds for the thread.
        thread.join(timeout=3600)
        # once the thread exits
        # if the thread is still running, its name will be changed to indicate that the thread is unresponsive.
        # if the thread exits, the next line does nothing.
        thread.name = f"{account.email} [hung]"


def check_then_run():
    logger.info("Checking if any accounts are ready...")
    accounts_ready = list()
    for account in db.read():
        if (datetime.datetime.now(tz=datetime.timezone.utc) - account.lastExec).total_seconds() >= \
                config.minimum_auto_rerun_delay_seconds:
            logger.info(f"{account.email} is ready.")
            accounts_ready.append(account)

        else:
            logger.info(f"{account.email} is not ready.")

    # run_sequential_threads(accounts=accounts_ready)


def main_screen(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


if __name__ == '__main__':
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=check_then_run, trigger="interval", seconds=20)
    # scheduler.start()
    # app.run(debug=not config.debug)
    # atexit.register(lambda: scheduler.shutdown())
    ft.app(target=main_screen)

# PB PASSWORD C!ddKm9R5ESTJJz6
#
"""

let vars = []

for (var b in window){
	if (window.hasOwnProperty(b)){
	vars.push(b)
{
}

vars.sort()
console.log(vars)

"""
