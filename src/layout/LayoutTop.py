import flet as ft

from layout.BaseLayout import BaseLayout
from pathlib import Path
from ui.FilesSearchbar import FilesSearchbar


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

        self.location_text = ft.Text(self.app.router.current_route, size=21)

        self.searchbar = FilesSearchbar(self.app, col={"xs": 12, "lg": 6})

        self.layout = ft.Column(
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

        self.app.events.route_changed.subscribe(self.on_route_change)

    def on_route_change(self, **_):
        self.buttonBack.disabled = len(self.app.router.history_backward) < 1
        self.buttonForward.disabled = len(self.app.router.history_forward) < 1
        self.location_text.value = str(Path(self.app.router.current_route).absolute())

        self.app.page.update()
