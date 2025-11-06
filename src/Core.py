import flet as ft

from router.FletRouter import FletRouter
from events.AppEvents import AppEvents
from mediaQuery.MediaQueryManager import MediaQueryManager
from utils.time import SetInterval
from pathlib import Path


class AppContext:
    app_running_seconds: int

    def __init__(
        self,
        page: ft.Page,
        router: FletRouter,
        events: AppEvents,
        media_query_manager: MediaQueryManager,
    ):
        self.app_root_path = str(Path(".").absolute())
        self.system = System(self.app_root_path)

        self.page = page
        self.router = router
        self.events = events
        self.media_query_manager = media_query_manager

        self.init_timer()

    def init_timer(self):
        def update_timer():
            self.app_running_seconds += 1

        self.app_running_seconds = 0
        SetInterval(update_timer, 1)


class System:
    protected_paths = []

    def __init__(self, app_root_path):
        self.app_root_path = app_root_path
        self.system_path = f"{self.app_root_path}/system"

        if not Path(self.system_path).exists():
            self.path = Path.mkdir(self.system_path)

        self.init_logging()
        self.init_folder("trash")

    def get_path(self, to_path):
        return f"{self.system_path}/{to_path}"

    def init_folder(self, f_name):
        folder_path = self.get_path(f_name)
        if not Path(folder_path).exists():
            Path.mkdir(folder_path)

    def init_logging(self):
        logs_path = self.get_path("app.log")
        if not Path(logs_path).exists():
            with open(logs_path, "w") as f:
                f.write("")
