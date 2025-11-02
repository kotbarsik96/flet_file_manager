import flet as ft

class MediaQueryManager:
    def __init__(self):
        self.breakpoints = {}
        self.listeners = {}
        self.current_break_point = None

    def on_resized(self, event: ft.WindowResizeEvent):
        self.check_for_updates(event.width)

    def check_for_updates(self, width):
        for name, (min_width, max_width) in self.breakpoints.items():
            if max_width >= width > min_width:
                if self.current_break_point != name:
                    self.current_break_point = name
                    for func in self.listeners[name]:
                        func()
