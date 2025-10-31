import flet as ft

from AppContext import AppContext


class LayoutBottom:
    control: ft.Text

    def __init__(self, app: AppContext):
        self.app = app
        self.init_layout()

    def init_layout(self):
        self.control = ft.Text("")
