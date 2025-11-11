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
            HotkeysDialog(page=self.page)

        if event.key == "F4":
            self.open_system_folder()

        if event.key == "F5":
            SpaceStatsDialog(self.page, self.system, self.router)
            
        if event.key == "F6":
            self.page.go("__Terminal__")

    def open_system_folder(self):
        self.page.go(str(self.system.system_path))
