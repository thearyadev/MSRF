import flet as ft


class Titlebar(ft.UserControl):
    def __init__(
            self,
            window_title: str = "",
            closable: bool = True,
            hidden: bool = False,
            visible: bool = True,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.window_title = window_title
        self.visible = visible
        self.closable = closable
        self.hidden = hidden

    def build(self):
        if self.hidden:
            return ft.Row(
                [
                    ft.WindowDragArea(
                        ft.Container(bgcolor=ft.colors.TRANSPARENT, padding=10, margin=0), expand=True),
                ]
            )
        else:
            return ft.Row(
                [
                    ft.WindowDragArea(
                        ft.Container(
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.icons.GENERATING_TOKENS, disabled=True),
                                    ft.Text(f"{self.window_title}")
                                ]
                            ), bgcolor=ft.colors.TRANSPARENT, padding=10, margin=0), expand=True
                    ),
                    ft.IconButton(ft.icons.CLOSE, on_click=lambda _: self.page.window_close())
                    if self.closable else ft.Container(),
                ],
                visible=self.visible
            )
