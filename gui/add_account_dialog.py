from typing import Callable

import flet as ft


class AddAccountDialog(ft.UserControl):
    def __init__(self, add_account_handler: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_account_handler = add_account_handler
        self.email_field = ft.TextField(label="Email", autofocus=True)
        self.password_field = ft.TextField(label="Password")
        self.sheet = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Add Account", size=35),
                        ft.Text(
                            "Note: Ensure that the Microsoft Rewards onboarding tasks have been completed. Make sure "
                            "the credentials are correct.", italic=True, color=ft.colors.BLUE_GREY),
                        ft.Text("Your account may be banned by Microsoft as this application is a direct violation of "
                                "their terms of service. Avoid using accounts that have any importance",
                                italic=True, color=ft.colors.RED,
                                tooltip="MSRF will attempt to avoid bans. This may not "
                                        "be successful, as MS Rewards will update "
                                        "faster than MSRF can. "),
                        ft.Row(
                            [
                                self.email_field,
                                self.password_field,
                                ft.ElevatedButton("Add",
                                                  on_click=self.add_btn_handler,
                                                  width=200,
                                                  height=60,
                                                  bgcolor=ft.colors.GREEN,
                                                  color=ft.colors.WHITE,
                                                  style=ft.ButtonStyle(
                                                      shape=ft.buttons.RoundedRectangleBorder(radius=5)
                                                  ))
                            ],

                        )
                    ],
                    tight=True,
                ),
                padding=10,
            ),
            open=False,
        )

    def show_dialog(self, *_):
        self.sheet.open = True
        self.sheet.update()

    def close_dialog(self, *_):
        self.sheet.open = False
        self.sheet.update()

    def add_btn_handler(self, *_):
        if not self.password_field.value:
            self.password_field.color = ft.colors.RED
            self.password_field.tooltip = "Please enter a password."
            self.password_field.update()
            return

        if not self.email_field.value:
            self.email_field.color = ft.colors.RED
            self.email_field.tooltip = "Please enter an email address."
            self.email_field.update()
            return

        if "@" not in self.email_field.value:
            self.email_field.color = ft.colors.RED
            self.email_field.tooltip = "Email is not valid."
            self.email_field.update()
            return

        # handle add account
        self.add_account_handler(email=self.email_field.value, password=self.password_field.value)
        self.page.update()
        self.close_dialog()

    def build(self):
        return self.sheet
