import flet as ft

from views.FletRouter import FletRouter

from layout.LayoutTop import LayoutTop
from layout.LayoutBottom import LayoutBottom


def main(page: ft.Page):
    fletRouter = FletRouter(page, ft)

    page.session.set("router", fletRouter)
    page.on_route_change = fletRouter.route_change
    page.go(".")

    page.add(LayoutTop(page))
    page.add(fletRouter.body)
    # page.add(LayoutBottom(page))


ft.app(main)
