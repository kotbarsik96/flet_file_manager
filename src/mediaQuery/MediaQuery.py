import flet as ft

from Core import AppContext

class MediaQuery:
    def __init__(self, app: AppContext):
        self.app = app

    def handler(self, event: ft.WindowResizeEvent):
        self.app.media_query_manager.on_resized(event)

    def on(self, point: str, callback_function: callable):
        self.app.media_query_manager.listeners[point].append(callback_function)
        self.app.media_query_manager.check_for_updates(self.app.page.width)

    def off(self, point: str, callback_function: callable):
        self.app.media_query_manager.listeners[point].remove(callback_function)

    def register(self, point: str, min_width: int, max_width: int):
        self.app.media_query_manager.breakpoints[point] = (min_width, max_width)
        self.app.media_query_manager.listeners[point] = []