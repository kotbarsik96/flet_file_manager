import flet as ft

from layout.BaseLayout import BaseLayout
from pathlib import Path


class LayoutTop(BaseLayout):
    def build_layout(self):
        self.buttonBack = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=lambda _: self.app.router.go_prev_route(),
        )
        self.buttonForward = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            on_click=lambda _: self.app.router.go_next_route(),
        )

        self.location_text = ft.Text(self.app.router.current_route)

        self.layout = ft.Row(
            [self.buttonBack, self.buttonForward, self.location_text],
        )

        self.app.events.route_changed.subscribe(self.on_route_change)

    def on_route_change(self, **_):
        self.buttonBack.disabled = len(self.app.router.history_backward) < 1
        self.buttonForward.disabled = len(self.app.router.history_forward) < 1
        self.location_text.value = str(Path(self.app.router.current_route).absolute())

        self.app.page.update()
