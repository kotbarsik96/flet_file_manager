import flet as ft

from view.BaseView import BaseView
from pathlib import Path
from ui.FilesSearchbar import FilesSearchbar
from Router import Router
from Events import AppEvents


class LayoutTop(BaseView):
    def __init__(self, page: ft.Page, router: Router, events: AppEvents):
        self.page = page
        self.router = router
        self.events = events
        
        self.build_view()
        events.keyboard.subscribe(self.handle_keyboard)
    
    def build_view(self):
        self.buttonBack = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=lambda _: self.router.go_prev_route(),
        )
        self.buttonForward = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            on_click=lambda _: self.router.go_next_route(),
        )

        self.location_text = ft.Text(self.router.current_route, size=21)

        self.searchbar = FilesSearchbar(page=self.page, router=self.router, col={"xs": 12, "lg": 6})

        self.view = ft.Column(
            [
                ft.ResponsiveRow(
                    [
                        ft.Row(
                            [self.buttonBack, self.buttonForward],
                            col=1
                        ),
                        self.searchbar.control,
                    ],
                    columns=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                self.location_text,
            ],
            spacing=20,
        )

        self.events.route_changed.subscribe(self.on_route_change)

    def on_route_change(self, **_):
        self.buttonBack.disabled = len(self.router.history_backward) < 1
        self.buttonForward.disabled = len(self.router.history_forward) < 1
        self.location_text.value = str(Path(self.router.current_route).absolute())

        self.page.update()

    def handle_keyboard(self, event: ft.KeyboardEvent):
        if event.key == "Arrow Left" and event.ctrl:
            self.handle_arrow_left(event)
        if event.key == "Arrow Right" and event.ctrl:
            self.handle_arrow_right(event)

    def handle_arrow_left(self, event: ft.KeyboardEvent):
        self.router.go_prev_route()

    def handle_arrow_right(self, event: ft.KeyboardEvent):
        self.router.go_next_route()