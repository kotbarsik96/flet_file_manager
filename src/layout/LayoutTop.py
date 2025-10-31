import flet as ft

from AppContext import AppContext


class LayoutTop:
    control: ft.Row
    
    def __init__(self, app: AppContext):
        self.app = app
        self.fletRouter = app.router
        self.init_layout()
        
    def init_layout(self):
        self.buttonBack = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=lambda _: self.fletRouter.go_prev_route(),
        )
        self.buttonForward = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            on_click=lambda _: self.fletRouter.go_next_route(),
        )
        
        self.location_text = ft.Text(self.fletRouter.current_route)
        
        self.control = ft.Row(
            [
                self.buttonBack,
                self.buttonForward,
                self.location_text
            ],
        )
        
        self.app.events.route_changed.subscribe(self.on_route_change)
        
    def on_route_change(self, **_):
        self.buttonBack.disabled = len(self.fletRouter.history_backward) < 1
        self.buttonForward.disabled = len(self.fletRouter.history_forward) < 1
        self.location_text.value = self.fletRouter.current_route

        self.app.page.update()
