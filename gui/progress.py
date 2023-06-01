import flet as ft


class Progress(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progressCircle = ft.ProgressRing(width=120, height=120, stroke_width=10)
        self.progressText = ft.Text("0%")

    def populate(self, new_value: float):
        self.progressText.value = f"{new_value * 100:.0f}%"
        self.progressCircle.value = new_value
        self.progressCircle.update()
        self.progressText.update()

    def build(self):
        return ft.Stack(
            controls=[
                ft.Column(
                    [
                        ft.Container(
                            width=45,
                            height=45,
                            content=self.progressText,
                            border_radius=50,
                            alignment=ft.alignment.center,
                        )
                    ],
                    left=37,
                    top=37,
                ),
                self.progressCircle,
            ]
        )
