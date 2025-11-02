import flet as ft

from router.FletRouter import FletRouter
from events.AppEvents import AppEvents
from mediaQuery.MediaQueryManager import MediaQueryManager


class AppContext:
    def __init__(
        self,
        page: ft.Page,
        router: FletRouter,
        events: AppEvents,
        media_query_manager: MediaQueryManager,
    ):
        self.page = page
        self.router = router
        self.events = events
        self.media_query_manager = media_query_manager
