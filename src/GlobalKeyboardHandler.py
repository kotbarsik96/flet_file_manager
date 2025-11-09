import flet as ft
from Events import AppEvents
from Core import System
from Router import Router

from ui.dialogs.MenuBarDialogs import HelpDialog, HotkeysDialog, SpaceStatsDialog


class GlobalKeyboardHandler:
    def __init__(
        self, system: System, events: AppEvents, page: ft.Page, router: Router
    ):
        self.system = system
        self.events = events
        self.page = page
        self.router = router
        events.keyboard.subscribe(self.handle_keyboard)

    def handle_keyboard(self, event: ft.KeyboardEvent):
        if event.key == "F3":
            self.open_hotkeys()

        if event.key == "F6":
            self.open_system_folder()

        if event.key == "F7":
            self.open_space_stats()

    def open_help(self):
        HelpDialog(page=self.page)

    def open_hotkeys(self):
        HotkeysDialog(page=self.page)

    def open_logs(self):
        pass

    def open_system_folder(self):
        self.page.go(str(self.system.system_path))

    def open_space_stats(self):
        SpaceStatsDialog(self.page, self.system, self.router)
