from typing import Callable

import flet as ft


class LogDisplay(ft.UserControl):
    def __init__(self, data_handler: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_handler = data_handler
        self.text = ft.Text("", font_family="Consolas", size=10, overflow=ft.TextOverflow.VISIBLE)
        self.populate()

    def populate(self):
        self.text.value = self.data_handler()
        try:
            self.text.update()
        except Exception:
            pass

    def build(self):
        return ft.Column(
            expand=True,
            controls=[self.text],
            scroll=ft.ScrollMode.ALWAYS,
        )
