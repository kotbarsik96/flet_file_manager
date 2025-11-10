import flet as ft
from view.BaseView import BaseView
from Core import System
from Events import AppEvents


class TerminalView(BaseView):
    def __init__(self, page: ft.Page, system: System, events: AppEvents):
        super().__init__(page=page, system=system, events=events)
        
        self.events.route_changed.subscribe(self.on_route_change)

    def on_mounted(self):
        pass
    
    def on_unmount(self):
        pass

    def build_view(self):
        pass
    