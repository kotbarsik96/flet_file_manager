import flet as ft

from router.FletRouter import FletRouter
from events.AppEvents import AppEvents
from mediaQuery.MediaQueryManager import MediaQueryManager
from utils.time import SetInterval


class AppContext:
    app_running_seconds: int
    
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
        
        self.init_timer()
        
    def init_timer(self):
        def update_timer():
            self.app_running_seconds += 1
        
        self.app_running_seconds = 0
        SetInterval(update_timer, 1)
        
