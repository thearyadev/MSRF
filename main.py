import atexit
import datetime
import os
import threading
import time

import flet as ft
import flet.buttons
from apscheduler.schedulers.background import BackgroundScheduler

import custom_logging
import database
import util
from gui import (AccountDataTable, AddAccountDialog, LogDisplay, Titlebar,
                 Toolbar, ToolbarItem)

try:
    os.mkdir("./errors")
except FileExistsError:
    pass

logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
config: util.Config = util.Config.load_config("configuration.yaml")  # load config from file
logger.info("Loaded ./configuration.yaml into config object")
db = database.DatabaseAccess()  # create database connection
logger.info("Connection to database was successful.")


def get_log() -> str:
    with open("farmer.log", "r") as file:
        return "".join(list((list(reversed(file.readlines()))[:100])))


def is_currently_running(account: util.MicrosoftAccount) -> bool:
    return bool(len([t.name for t in threading.enumerate() if t.name == account.email]))


def toggle_debug_mode(_):
    config.debug = not config.debug


def remove_account(email):
    logger.info(f"Removing {email}")
    account = [a for a in db.read() if a.email == email]
    if len(account):
        db.delete(account[0])


def add_account(email, password):
    logger.info(f"Adding {email}")
    print(password)
    # if current account number is less than or equal to the max allowed accounts
    if len(db.read()) <= config.max_account_number:
        db.insert(util.MicrosoftAccount(
            email=email,
            password=password,
            lastExec=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=365),
            points=0
        ))
    else:
        logger.error(f"Unable to add account {email}. Account limit reached.")


def force_exec(_):
    accounts = db.read()
    for account in accounts:
        account.lastExec = account.lastExec - datetime.timedelta(days=365)
        db.write(account)


def force_exec_single(event: flet.control_event.ControlEvent):
    accounts = db.read()
    for account in accounts:
        if account.id == event.control.content.data:
            account.lastExec = account.lastExec - datetime.timedelta(days=365)
            db.write(account)
            return


def pick_and_run():
    running = bool([t.name for t in threading.enumerate() if "@" in t.name])  # get all active threads by name
    # the thread names that are active account processes will have an @ in them.
    # if true, there is something running.

    if not running:

        # 1. Sort accounts by last exec datetime.
        # 2 if the time between its last execution and now is greater than the defined # of seconds
        # 3. append
        validAccounts = [
            account for account in sorted(db.read(), key=lambda a: a.lastExec)
            if (
                       datetime.datetime.now(tz=datetime.timezone.utc) - account.lastExec
               ).total_seconds() > config.minimum_auto_rerun_delay_seconds
        ]
        if validAccounts:  # if at least one account is eligible
            threading.Thread(
                name=validAccounts[0].email,
                target=util.exec_farmer,
                kwargs={
                    "account": validAccounts[0],
                    "config": config,
                    "db": db
                }
            ).start()
            logger.info(f"Started thread for: {validAccounts[0]}")
            return
        logger.info("Eligible account was not found.")
        return


def configure_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=pick_and_run, trigger="interval", seconds=15)
    if config.run_scheduler:
        scheduler.start()
        atexit.register(scheduler.shutdown)


def main_screen(page: ft.Page):
    def hydrate():
        time.sleep(config.hydration_rate)
        accountsControl.accounts = db.read()
        accountsControl.populate()
        logDisplay.populate()
        page.update()

    def toggle_dark(_):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()
            config.theme_mode = "LIGHT"
            config.save_config("configuration.yaml")
            return

        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.update()
            config.theme_mode = "DARK"
            config.save_config("configuration.yaml")
            return
        page.theme_mode = ft.ThemeMode.DARK
        config.theme_mode = "DARK"
        config.save_config("configuration.yaml")
        page.update()
        return

    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_opacity = config.gui_window_opacity
    page.theme_mode = config.theme_mode.lower()
    page.title = "Microsoft Rewards Farmer"
    page.window_height = 720
    page.window_width = 1280
    page.window_resizable = False
    page.window_maximizable = False

    addAccountDialog = AddAccountDialog(add_account_handler=add_account)
    page.overlay.append(addAccountDialog)

    logDisplay = LogDisplay(data_handler=logger.load)

    accountsControl = AccountDataTable(
        accounts=db.read(),
        force_single_account_callback=force_exec_single,
        delete_account_handler=remove_account
    )
    version: util.VersionInfo = util.check_version()
    updatePrompt = update_prompt = ft.Text("")
    if version.release_version != config.version:
        updatePrompt = ft.TextButton(
            "Update Available",
            icon=ft.icons.UPDATE,
            icon_color=ft.colors.GREEN,
            tooltip=f"You are currently on {config.version}.\n"
                    f"\n{version.release_version} is available in the latest release for thearyadev/msrf."
                    f"Click this button to open",
            on_click=lambda _: page.launch_url(version.release_url)
        )
    if "DEV" in config.version:
        updatePrompt = ft.TextButton(
            "Development Build",
            icon=ft.icons.LOGO_DEV,
            icon_color=ft.colors.GREEN,
            disabled=True
        )

    page.add(
        Titlebar("Microsoft Rewards Farmer", visible=not page.web),
        ft.Row(
            [
                ft.Column(
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=accountsControl,
                            expand=True,
                        ),
                        ft.Text("The farmer is paused." if not config.run_scheduler else ""
                                , italic=True, color=ft.colors.BLUE_GREY),
                        Toolbar(
                            toolbarItems=[
                                ToolbarItem(
                                    icon=ft.icons.ADD,
                                    tooltip="Add Account",
                                    callback=addAccountDialog.show_dialog
                                ),
                                ToolbarItem(
                                    icon=ft.icons.DARK_MODE_SHARP,
                                    tooltip="Toggle Dark Mode",
                                    callback=toggle_dark
                                ),
                                ToolbarItem(
                                    icon=ft.icons.BUG_REPORT,
                                    tooltip="Debugging Mode",
                                    callback=toggle_debug_mode
                                ),
                                ToolbarItem(
                                    icon=ft.icons.DOUBLE_ARROW,
                                    tooltip="Force Execution (Not Recommended)",
                                    callback=force_exec
                                ),
                                ToolbarItem(
                                    icon=ft.icons.FOLDER_SPECIAL,
                                    tooltip="Open Program Folder",
                                    callback=lambda _: os.startfile(".")
                                )
                            ],
                            update_prompt=updatePrompt
                        )
                    ],

                ),
                ft.VerticalDivider(),
                logDisplay
            ],
            spacing=0,
            expand=True,
        )
    )

    page.window_visible = True

    while True:
        hydrate()


def main():
    configure_scheduler()
    ft.app(target=main_screen, view=ft.FLET_APP_HIDDEN)


if __name__ == '__main__':
    main()
