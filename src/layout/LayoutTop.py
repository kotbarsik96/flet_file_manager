import flet as ft

from AppContext import AppContext


def LayoutTop(app: AppContext):
    fletRouter = app.router

    buttonBack = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        on_click=lambda _: fletRouter.go_prev_route(),
    )
    buttonForward = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT,
        on_click=lambda _: fletRouter.go_next_route(),
    )

    leading = ft.Row(
        [
            buttonBack,
            buttonForward,
        ],
    )

    def set_buttons_state(**_):
        buttonBack.disabled = len(fletRouter.history_backward) < 1
        buttonForward.disabled = len(fletRouter.history_forward) < 1

        app.page.update()

    app.events.route_changed.subscribe(set_buttons_state)

    return leading
