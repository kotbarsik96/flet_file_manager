import flet as ft
import time
from utils.time import format_seconds, SetInterval
from Core import System


class TimerStyles:
    def __init__(self):
        self.font_size = 18


timer_styles = TimerStyles()


class TimerOS:
    def __init__(self, page: ft.Page):
        self.page = page
        self.timer_text = ft.Text(
            format_seconds(time.monotonic()), size=timer_styles.font_size
        )
        self.interval = SetInterval(self.update_timer, 1)
        self.timer_text.will_unmount = self.on_unmount

    def update_timer(self):
        self.timer_text.value = format_seconds(time.monotonic())
        self.page.update()

    def on_unmount(self, *_):
        self.interval.cancel()


class TimerApp:
    def __init__(self, page: ft.Page, system: System):
        self.page = page
        self.system = system
        self.timer_text = ft.Text(
            format_seconds(self.system.app_running_seconds), size=timer_styles.font_size
        )
        self.interval = SetInterval(self.update_timer, 1)
        self.timer_text.will_unmount = self.on_unmount

    def update_timer(self):
        self.timer_text.value = format_seconds(self.system.app_running_seconds)
        self.page.update()
        
    def on_unmount(self, *_):
        self.interval.cancel() 