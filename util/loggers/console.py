from rich.console import Console
from deprecated import deprecated


@deprecated(version='beta', reason="python builtin logger is used. 'msrf'")
class ConsoleLogger(Console):
    def __init__(self, file_path: str, *args, **kwargs):
        super().__init__(record=True, *args, **kwargs)
        self.file_path = file_path

    def log(self, *args, **kwargs):
        super().log(*args, **kwargs)
        super().save_text(self.file_path, clear=False)


