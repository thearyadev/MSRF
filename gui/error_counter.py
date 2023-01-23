import os

import flet as ft


class ErrorCounter(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = ft.TextButton(
            "Errors",
            icon=ft.icons.ERROR_SHARP,
            tooltip="Some errors have been detected.\nOpen the project directory to view them.",
            visible=False,
            icon_color=ft.colors.RED
        )
        self.populate()

    @staticmethod
    def count_errors() -> int:
        return len([f for f in os.listdir("errors") if "error" in f])

    def populate(self):
        eCount = self.count_errors()
        self.prompt.text = f"{eCount} Errors"
        if eCount:
            self.prompt.visible = True
        else:
            self.prompt.visible = False
        try:
            self.prompt.update()
        except Exception:
            pass

    def build(self):
        return self.prompt
