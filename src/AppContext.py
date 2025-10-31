import flet as ft

from router.FletRouter import FletRouter
from events.AppEvents import AppEvents


class AppContext:
    page: ft.Page
    router: FletRouter
    events: AppEvents

    def __init__(self, page: ft.Page, router: FletRouter, events: AppEvents):
        self.page = page
        self.router = router
        self.events = events
