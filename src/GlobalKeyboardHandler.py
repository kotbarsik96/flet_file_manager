import flet as ft
from Events import AppEvents
from Core import System

from ui.dialogs.MenuBarDialogs import HelpDialog, HotkeysDialog


class GlobalKeyboardHandler:
    def __init__(self, system: System, events: AppEvents, page: ft.Page):
        self.system = system
        self.events = events
        self.page = page
        events.keyboard.subscribe(self.handle_keyboard)

    def handle_keyboard(self, event: ft.KeyboardEvent):
        if event.key == "F3":
            self.open_hotkeys()

    def open_help(self):
        HelpDialog(page=self.page)
        
    def open_hotkeys(self):
        HotkeysDialog(page=self.page)

    def open_logs(self):
        pass
