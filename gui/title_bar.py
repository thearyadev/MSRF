import flet as ft


class Titlebar(ft.UserControl):
    def __init__(self, window_title: str = "", visible: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_title = window_title
        self.visible = visible

    def build(self):
        return ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(ft.Text(f"{self.window_title}"),
                                 bgcolor=ft.colors.TRANSPARENT, padding=10, margin=0), expand=True
                ),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: self.page.window_close()),
            ],
            visible=self.visible
        )
