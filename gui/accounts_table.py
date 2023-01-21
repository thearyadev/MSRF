import datetime
import threading
from typing import TYPE_CHECKING, Callable

import flet as ft

if TYPE_CHECKING:
    import util


def is_currently_running(account: 'util.MicrosoftAccount') -> bool:
    return bool(len([t.name for t in threading.enumerate() if t.name == account.email]))


def calc_hours_ago(account: 'util.MicrosoftAccount') -> str:
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


class AccountDataTable(ft.UserControl):
    def __init__(
            self,
            force_single_account_callback: Callable,
            delete_account_handler: Callable,
            accounts: list['util.MicrosoftAccount'],
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.force_single_account_callback = force_single_account_callback
        self.accounts = accounts
        self.delete_account_dialog = DeleteAccountDialog(delete_account_handler)
        self.table = ft.DataTable(
            width=600,
            horizontal_lines=ft.border.BorderSide(width=0, color=ft.colors.BLACK26),
            divider_thickness=0,
            columns=[
                ft.DataColumn(ft.Text("Account"), tooltip="Long press the account name to delete."),
                ft.DataColumn(ft.Text("Last Exec"),
                              tooltip="Long press on the Last Exec of the account you want to run now."),
                ft.DataColumn(ft.Text("Points"), numeric=True),
            ],
            rows=[]
        )
        self.addAccountPrompt = AddAccountPrompt()
        self.row = ft.Row(
            controls=[
                self.table if self.accounts else self.addAccountPrompt,
                self.delete_account_dialog
            ],
        )
        self.populate()

    def handle_account_long_press(self, event):
        self.delete_account_dialog.current_account = event.control.content.value
        self.delete_account_dialog.show()

    def populate(self):
        self.table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(account.email),
                        on_long_press=self.handle_account_long_press
                        if not is_currently_running(
                            account) else None,
                    ),
                    ft.DataCell(
                        ft.Text(calc_hours_ago(account), data=account.id),
                        on_long_press=self.force_single_account_callback if not is_currently_running(
                            account) else None,
                    ),
                    ft.DataCell(ft.Text(str(account.points))),
                ]

            ) for account in self.accounts
        ]
        self.row.controls = [
            self.table if self.accounts else self.addAccountPrompt,
            self.delete_account_dialog
        ]

        try:
            self.row.update()
            self.table.update()
        except Exception:
            pass  # this will throw an exception when the component is not on the page yet.

    def build(self):
        return self.row


class AddAccountPrompt(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        return ft.Text(
            "Click the + button to add an account.",
            width=600,
            text_align=ft.TextAlign.CENTER
        )


class DeleteAccountDialog(ft.UserControl):
    def __init__(self, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = handler
        self.dialog = ft.AlertDialog(
            title=ft.Text("Remove Account"),
            modal=True,
            actions=[
                ft.TextButton("Yes", on_click=self.close, data=True),
                ft.TextButton("No", on_click=self.close, data=False)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.current_account: str | None = None

    def show(self, *_):
        self.dialog.open = True
        self.dialog.update()

    def close(self, event):

        if event.control.data:
            if self.current_account:
                self.handler(self.current_account)
        self.dialog.open = False
        self.dialog.update()

    def build(self):
        return self.dialog
