import flet as ft
from Core import AppContext


class BaseLayout:
    layout: ft.Control

    def __init__(self, app: AppContext):
        self.app = app
        self.build_layout()

    def build_layout(self):
        self.layout = ft.Text("")
