import flet as ft

from views.FletRouter import FletRouter


def LayoutTop(page: ft.Page):
    fletRouter: FletRouter = page.session.get("router")

    def historyBackward():
        if len(fletRouter.history_backward) > 0 and fletRouter.history_backward[-1]:
            page.go(fletRouter.history_backward[-1])

    def historyForward():
        if len(fletRouter.history_forward) > 0 and fletRouter.history_forward[0]:
            page.go(fletRouter.history_forward[0])

    leading = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                on_click=lambda _: historyBackward(),
            ),
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                on_click=lambda _: historyForward(),
            ),
        ]
    )

    return ft.AppBar(leading=leading)
