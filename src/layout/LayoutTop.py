import flet as ft

from AppContext import AppContext

def LayoutTop(app: AppContext):
    fletRouter = app.router

    leading = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                on_click=lambda _: fletRouter.go_prev_route(),
            ),
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                on_click=lambda _: fletRouter.go_next_route(),
            ),
        ],
    )

    return leading
