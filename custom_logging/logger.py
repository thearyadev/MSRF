from enum import Enum
import inspect
import threading
import rich

from _testcapi import instancemethod

import custom_logging


class LogLevel(Enum):
    INFO = 1
    DEBUG = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


lock = threading.Lock()


class FileStreamLogger:
    def __init__(self, *,
                 console: bool = True,
                 colors: bool = False,
                 file_path: str = "./log.txt",
                 logLevel: LogLevel = LogLevel.CRITICAL):
        self.console: bool = console
        self.colors: bool = colors
        self.logLevel: LogLevel = logLevel
        self.file_path: str = file_path
        self.file = open(self.file_path, "a")

    def _log(self, level: LogLevel, message: str) -> None:
        next_in_line_frame = inspect.stack()[2]
        lineNo: int = next_in_line_frame.lineno
        function: str = f"<{next_in_line_frame.function}>"
        threadName: str = f"<{threading.current_thread().name}>"
        output_message: str = f"[{LogLevel(level).name}][{threadName}][{function}][Line {lineNo}] {message}"
        lock.acquire()
        self.file.write(output_message + "\n")
        self.file.flush()
        lock.release()
        if self.colors and self.console:
            match level:
                case LogLevel.INFO:
                    rich.print("[cyan]" + output_message)
                    return None
                case LogLevel.DEBUG:
                    rich.print("[green]" + output_message)
                    return None
                case LogLevel.WARNING:
                    rich.print("[yellow]" + output_message)
                    return None
                case LogLevel.ERROR:
                    rich.print("[red]" + output_message)
                    return None
                case LogLevel.CRITICAL:
                    rich.print("[red bold]" + output_message)
                    return None
        if self.console:
            match level:
                case LogLevel.INFO:
                    rich.print("[white]" + output_message)
                    return None
                case LogLevel.DEBUG:
                    rich.print("[white]" + output_message)
                    return None
                case LogLevel.WARNING:
                    rich.print("[white]" + output_message)
                    return None
                case LogLevel.ERROR:
                    rich.print("[white]" + output_message)
                    return None
                case LogLevel.CRITICAL:
                    rich.print("[white]" + output_message)
                    return None

    def info(self, *message) -> None:
        self._log(level=LogLevel.INFO, message=" ".join(message))

    def debug(self, *message) -> None:
        self._log(level=LogLevel.DEBUG, message=" ".join(message))

    def warning(self, *message) -> None:
        self._log(level=LogLevel.WARNING, message=" ".join(message))

    def error(self, *message) -> None:
        self._log(level=LogLevel.ERROR, message=" ".join(message))

    def critical(self, *message) -> None:
        self._log(level=LogLevel.CRITICAL, message=" ".join(message))


def fonc():
    logger.info("hello", "world")
    logger2.debug("hello", "world")
    logger3.warning("hello", "world")
    logger2.error("hello", "world")
    logger3.critical("hello", "world")


def main():
    logger.info("hello", "world")
    logger2.debug("hello", "world")
    logger3.warning("hello", "world")
    logger2.error("hello", "world")
    logger3.critical("hello", "world")
    fonc()


if __name__ == '__main__':
    logger = FileStreamLogger(console=True, colors=True)
    logger2 = FileStreamLogger(console=True, colors=True)
    logger3 = FileStreamLogger(console=True, colors=True)

    for i in range(3):
        threading.Thread(target=main, name="thread" + str(i)).start()
