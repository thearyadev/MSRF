from rich.console import Console


class ConsoleLogger(Console):
    def __init__self(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log(self, *args, **kwargs):
        super().log(*args, **kwargs)

