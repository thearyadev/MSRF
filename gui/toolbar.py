import flet as ft
from typing import Callable


class ToolbarItem(ft.UserControl):

    def __init__(self, tooltip: str = "", callback: Callable = None, icon: str = ft.icons.STAR, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tooltip = tooltip
        self.callback = callback
        self.icon = icon

    def build(self):
        return ft.IconButton(
            icon=self.icon,
            tooltip=self.tooltip,
            on_click=self.callback
        )


class Toolbar(ft.UserControl):
    def __init__(self, toolbarItems: list[ToolbarItem], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toolbarItems = toolbarItems

    def build(self):
        return ft.Row(self.toolbarItems)
