import datetime
import threading
import time
import util
from rich import print
import database
import logging
import sys
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
import flet as ft
"""
github.com/thearyadev/msrf

What does this file do? 

1. Configures logging
2. Connects to Database
3. Configures and runs UI/Flet server. 
4. methods for starting and managing farmer processes using sequentially run threads
5. background scheduler to check which accounts are ready to run
"""

def configure_loggers():
    logging.basicConfig(
        format='[%(threadName)s] [%(levelname)s]'
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

    if len([t.name for t in threading.enumerate() if "@" in t.name]):
        logger.warning("Attempted to start sequential thread process"
                       " while existing process is already running. Cancelled.")
        return

    run_sequential_threads(accounts=accounts_ready)


def get_log() -> str:
    with open("farmer.log", "r") as file:
        return "".join(list((list(reversed(file.readlines()))[:100])))


def is_currently_running(account: util.MicrosoftAccount) -> bool:
    c = bool(len([t.name for t in threading.enumerate() if t.name == account.email]))

    return c


def remove_account(email):
    logger.info(f"Removing {email}")


def main_screen(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    page.window_opacity = config.gui_window_opacity
    page.theme_mode = "light"

    def show_bs(e):
        bs.open = True
        bs.update()

    def bs_dismissed(e):
        ...

    def close_bs(e):
        bs.open = False
        bs.update()

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Add Account", size=35),
                    ft.Text("Note: Ensure that the Microsoft Rewards onboarding tasks have been completed. Make sure "
                            "the credentials are correct.", italic=True, color=ft.colors.BLUE_GREY),
                    ft.Text("Your account may be banned by Microsoft as this application is a direct violation of "
                            "their terms of service.", italic=True, color=ft.colors.RED),
                    ft.Row(
                        [
                            ft.TextField(label="Email", autofocus=True),
                            ft.TextField(label="Password"),
                            ft.ElevatedButton("Add", on_click=close_bs)
                        ],

                    )
                ],
                tight=True,
            ),
            padding=10,
        ),
        open=False,
        on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)

    page.title = "Microsoft Rewards Farmer"
    page.window_height = 720
    page.window_width = 1280
    page.window_resizable = False
    page.window_maximizable = False

    log_text = ft.Text(get_log(), font_family="Consolas", size=10, overflow=ft.TextOverflow.VISIBLE)
    accountsTable = ft.DataTable(
        width=600 if not page.web else 800,
        horizontal_lines=ft.border.BorderSide(width=0, color=ft.colors.BLACK26),
        divider_thickness=0,
        columns=[
            ft.DataColumn(ft.Text("Account")),
            ft.DataColumn(ft.Text("Last Exec")),
            ft.DataColumn(ft.Text("Points"), numeric=True),
            ft.DataColumn(ft.Text("")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(account.email)),
                    ft.DataCell(
                        ft.Text(
                            f"{(((datetime.datetime.now(tz=datetime.timezone.utc) - account.lastExec).total_seconds() / 60) / 60):.0f} hrs ago"
                            if not is_currently_running(account)
                            else "Currently Running"
                        )),
                    ft.DataCell(ft.Text(str(account.points))),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            tooltip="Remove Account",
                            on_click=lambda e: [remove_account(e.control.data), hydrate()],
                            data=account.email
                        )
                    )
                ]

            ) for account in db.read()
        ],
    )

    log_display = ft.Column(
        expand=True,
        controls=[log_text],
        scroll=ft.ScrollMode.ALWAYS,
    )
    divider = ft.VerticalDivider()

    def toggle_dark(_):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()
            return

        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.update()
            return
        page.theme_mode = ft.ThemeMode.DARK
        page.update()
        return

    def toggle_log(_):
        if not log_display.visible:
            # if log is disabled
            log_display.visible = True
            accountsTable.width = 600
            divider.visible = True
            page.update()
            return
        # if log is enabled
        log_display.visible = False
        accountsTable.width = 1240
        divider.visible = False
        page.update()
        return

    page.add(
        ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(ft.Text("Microsoft Rewards Farmer"),
                                 bgcolor=ft.colors.TRANSPARENT, padding=10, margin=0), expand=True
                ),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close()),
            ],
            visible=not page.web,
        ),

        ft.Row(
            [

                ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.STAR_PURPLE500_SHARP,
                                    tooltip="View Project on GitHub",
                                    on_click=lambda _: page.launch_url("https://github.com/thearyadev/MSRF")
                                ),
                                ft.Text("thearyadev", color=ft.colors.BLUE_GREY, italic=True)
                            ],
                            spacing=0
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=accountsTable,
                            expand=True,
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.ADD,
                                    tooltip="Add Account",
                                    on_click=show_bs
                                ),
                                ft.IconButton(
                                    icon=ft.icons.TOGGLE_ON,
                                    tooltip="Toggle Log Display",
                                    on_click=toggle_log,
                                    visible=not page.web
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DARK_MODE_SHARP,
                                    tooltip="Toggle Dark Mode",
                                    on_click=toggle_dark,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.LOCK_RESET,
                                    tooltip="Reset Configuration",
                                    on_click=toggle_dark,
                                ),
                                ft.Text("Server Mode" if config.operation_mode == "SERVER" else "Application Mode",
                                        italic=True,
                                        color=ft.colors.RED,
                                        tooltip="Application Mode:\nMSRF will run as a desktop application. This is "
                                                "very similar to the server instance, but it enables use as an app on "
                                                "your computer. This can be left running in the background, "
                                                "or started as needed. \nOnce launched, MSRF will auto start the "
                                                "farming process after a few seconds.\nAvoid closing the application "
                                                "if any account states 'Currently Running', as this will cancel the "
                                                "execution and cause MSRF to wait another day to run that "
                                                "account.\n\nServer Mode:\nMSRF will run on a high uptime server "
                                                "instance. This is similar to application mode, but the interface "
                                                "will be available though the web instead. "
                                        )
                            ],
                        )
                    ],

                ),
                divider,
                log_display,
            ],
            spacing=0,
            expand=True,
        )
    )

    def hydrate():
        accountsTable.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(account.email)),
                    ft.DataCell(
                        ft.Text(
                            f"{(((datetime.datetime.now(tz=datetime.timezone.utc) - account.lastExec).total_seconds() / 60) / 60):.0f} hrs ago"
                            if not is_currently_running(account)
                            else "Currently Running"
                        )
                    ),
                    ft.DataCell(ft.Text(str(account.points))),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            tooltip="Remove Account",
                            on_click=lambda e: [remove_account(e.control.data), hydrate()],
                            data=account.email
                        )
                    )
                ]

            ) for account in db.read()
        ]

        log_text.value = get_log()
        page.update()

    page.window_visible = True
    page.window_center()

    while True:
        time.sleep(4)
        hydrate()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_then_run, trigger="interval", seconds=30)
    # scheduler.start()

    ft.app(target=main_screen, view=ft.WEB_BROWSER if config.operation_mode == "SERVER" else "flet_app_hidden")
    atexit.register(lambda: scheduler.shutdown())
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
