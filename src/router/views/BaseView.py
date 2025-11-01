import flet as ft
from AppContext import AppContext


class BaseView:
    view: ft.Control

    def __init__(self, app: AppContext):
        self.app = app
        self.build_view()

    def build_view(self):
        self.view = ft.Text("")
