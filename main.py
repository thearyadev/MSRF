import atexit
import copy
import datetime
import os
import threading
import time

import flet as ft
import flet.buttons
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

import custom_logging
import database
import util

"""
github.com/thearyadev/msrf

What does this file do?

1. Configures logging
2. Connects to Database
3. Configures and runs UI/Flet server.
4. methods for starting and managing farmer processes using sequentially run threads
5. background scheduler to check which accounts are ready to run

Also... idk how to build ui's. this file is messy.
"""

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


def calc_hours_ago(account: util.MicrosoftAccount) -> str:
    tsec = (
            datetime.datetime.now(tz=datetime.timezone.utc) - account.lastExec.astimezone(tz=datetime.timezone.utc)
    ).total_seconds()

    if tsec > 2_592_000:
        return "Ready (Waiting)"

    if is_currently_running(account):
        return "Currently Running"
    thour = tsec / 60 / 60
    if thour < 1:
        return "Recently"
    return f"{tsec / 60 / 60:.0f} hrs ago"


def force_exec():
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


def main_screen(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    page.window_opacity = config.gui_window_opacity
    page.theme_mode = config.theme_mode.lower()

    def show_bs(_):
        bs.open = True
        bs.update()

    def bs_dismissed(_):
        ...

    def close_bs(_):
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
                            "their terms of service. Avoid using accounts that have any importance",
                            italic=True, color=ft.colors.RED, tooltip="MSRF will attempt to avoid bans. This may not "
                                                                      "be successful, as MS Rewards will update "
                                                                      "faster than MSRF can. "),
                    ft.Row(
                        [
                            email_field := ft.TextField(label="Email", autofocus=True),
                            password_field := ft.TextField(label="Password"),
                            ft.ElevatedButton("Add",
                                              on_click=lambda _: [close_bs(_), add_account_btn_handler(), hydrate()],
                                              width=200,
                                              height=60,
                                              bgcolor=flet.colors.GREEN,
                                              color=flet.colors.WHITE,
                                              style=ft.ButtonStyle(
                                                  shape=flet.buttons.RoundedRectangleBorder(radius=5)
                                              ))
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

    def add_account_btn_handler():
        if not email_field.value:
            return

        if not password_field.value:
            return

        if "@" not in email_field.value:
            return

        e, p = copy.copy(email_field.value), copy.copy(password_field.value)
        email_field.value = ""
        password_field.value = ""
        page.update()
        add_account(e, p)

    page.overlay.append(bs)

    page.title = "Microsoft Rewards Farmer"
    page.window_height = 720
    page.window_width = 1280
    page.window_resizable = False
    page.window_maximizable = False

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

    def show_del_acct_dialog(e):
        delete_account_dialog.data = e.control.content.value
        page.dialog = delete_account_dialog
        delete_account_dialog.open = True
        page.update()

    def hide_del_acct_dialog(e):

        delete_account_dialog.open = False
        page.update()
        if e.control.data:
            remove_account(delete_account_dialog.data)
        delete_account_dialog.data = ""

    log_text = ft.Text(logger.load(), font_family="Consolas", size=10, overflow=ft.TextOverflow.VISIBLE)
    add_account_prompt = ft.Text("Click the + button below to add an account.",
                                 width=600,
                                 text_align=ft.TextAlign.CENTER)
    accountsTable = ft.DataTable(
        width=600 if not page.web else 800,
        horizontal_lines=ft.border.BorderSide(width=0, color=ft.colors.BLACK26),
        divider_thickness=0,
        columns=[
            ft.DataColumn(ft.Text("Account"), tooltip="Long press the account name to delete."),
            ft.DataColumn(ft.Text("Last Exec"),
                          tooltip="Long press on the Last Exec of the account you want to run now."),
            ft.DataColumn(ft.Text("Points"), numeric=True),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(account.email),
                                on_long_press=show_del_acct_dialog if not is_currently_running(account) else None),
                    ft.DataCell(
                        ft.Text(calc_hours_ago(account), data=account.id),
                        on_long_press=force_exec_single if not is_currently_running(account) else None,
                    ),
                    ft.DataCell(ft.Text(str(account.points))),
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

    delete_account_dialog = ft.AlertDialog(
        title=ft.Text("Remove Account"),
        modal=True,
        actions=[
            ft.TextButton("Yes", on_click=hide_del_acct_dialog, data=True),
            ft.TextButton("No", on_click=hide_del_acct_dialog, data=False),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def toggle_log(_):
        if not log_display.visible:
            # if log is disabled
            log_display.visible = True
            accountsTable.width = 600
            add_account_prompt.width = 600
            divider.visible = True
            page.update()
            return
        # if log is enabled
        log_display.visible = False
        accountsTable.width = 1240
        add_account_prompt.width = 1240
        divider.visible = False
        page.update()
        return

    version_info: util.VersionInfo = util.check_version()
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
                        accounts_container := ft.Container(
                            alignment=ft.alignment.center,
                            content=accountsTable if len(db.read()) else add_account_prompt,
                            expand=True,
                        ),
                        ft.Row(
                            [
                                bg_process_prompt := ft.Text("",
                                                             color=ft.colors.BLUE_GREY, italic=True)
                            ]
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
                                    icon=ft.icons.BUG_REPORT,
                                    tooltip="Debugging Mode",
                                    on_click=toggle_debug_mode,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DOUBLE_ARROW,
                                    tooltip="Force Execution (Not Recommended)",
                                    on_click=lambda _: force_exec(),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.FOLDER_SPECIAL,
                                    tooltip="Open Program Folder",
                                    on_click=lambda _: os.startfile(".")
                                ),
                                ft.Container(
                                    content=ft.Text("Update Available",
                                                    color=ft.colors.RED,
                                                    tooltip=f"Version {version_info.release_version} is available."
                                                            f" Currently on {config.version}"
                                                            f".\nClick to update") if
                                    version_info.release_version != config.version else None,
                                    on_click=lambda _: page.launch_url(version_info.release_url)
                                ) if "DEVELOPMENT" not in config.version else
                                ft.Container(
                                    content=ft.Text("DEVELOPMENT BUILD",
                                                    style=ft.TextThemeStyle.BODY_MEDIUM,
                                                    color=ft.colors.GREEN)
                                )

                            ],
                        )
                    ],

                ),
                divider,
                log_display
            ],
            spacing=0,
            expand=True,
        )
    )
    page.client_storage.set("farmer_prompt_shown", False)

    def hydrate():
        accountsTable.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(account.email),
                                on_long_press=show_del_acct_dialog if not is_currently_running(account) else None),
                    ft.DataCell(
                        ft.Text(calc_hours_ago(account), data=account.id),
                        on_long_press=force_exec_single if not is_currently_running(account) else None,
                    ),
                    ft.DataCell(ft.Text(str(account.points))),
                ]

            ) for account in db.read()
        ]

        log_text.value = logger.load()
        accounts_container.content = accountsTable if len(accountsTable.rows) else add_account_prompt

        if not page.client_storage.get("farmer_prompt_shown"):
            try:
                secs = (
                        scheduler.get_jobs()[0]
                        .next_run_time - datetime.datetime.now(tz=pytz.timezone('America/New_York'))
                ).total_seconds()
                if secs < 1.5:
                    page.client_storage.set("farmer_prompt_shown", True)

                bg_process_prompt.value = f"Starting Farmer in: {secs:.0f} seconds"

            except Exception:
                bg_process_prompt.value = "Paused"
        else:
            bg_process_prompt.value = ""

        page.update()

    page.window_visible = True

    while True:
        time.sleep(config.hydration_rate)
        hydrate()


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


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=pick_and_run, trigger="interval", seconds=15)
    if config.run_scheduler:
        scheduler.start()

    ft.app(target=main_screen, view=ft.FLET_APP_HIDDEN)
    atexit.register(scheduler.shutdown)
