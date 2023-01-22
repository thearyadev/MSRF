from typing import Callable

import flet as ft


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
    def __init__(
            self,
            toolbarItems: list[ToolbarItem | ft.control.Control],
            update_prompt: ft.control.Control | None = None,
            error_prompt: ft.control.Control | None = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.toolbarItems = toolbarItems
        if update_prompt:
            self.toolbarItems.append(update_prompt)

        if error_prompt:
            self.toolbarItems.append(error_prompt)

    def build(self):
        return ft.Row(self.toolbarItems)
