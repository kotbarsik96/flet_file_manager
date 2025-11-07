import flet as ft
from pathlib import Path
from utils.time import SetInterval
import shutil
import logging
from logging.handlers import WatchedFileHandler


class System:
    app_running_seconds: int
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.system_path = root_path / "system"
        self.system_path.mkdir(parents=True, exist_ok=True)
        self.trash = Trash(self.system_path)
        self.logger = Logger(self.system_path)
        self.init_timer()

    def init_timer(self):
        def update_timer():
            self.app_running_seconds += 1

        self.app_running_seconds = 0
        SetInterval(update_timer, 1)


class Trash:
    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.path = self.system_path / "trash"
        self.path.mkdir(parents=True, exist_ok=True)

    def add(self, path: Path):
        return Path(shutil.move(str(path), str(self.path)))


class Logger:
    def __init__(self, system_path: Path):
        self.system_path = system_path
        self.path = self.system_path / "app.log"
        self.path.touch(exist_ok=True)

        self.init_logger()

    def init_logger(self):
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.INFO)
        self.handler = WatchedFileHandler(self.path, encoding="utf-8")
        self.handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        self.logger.addHandler(self.handler)
