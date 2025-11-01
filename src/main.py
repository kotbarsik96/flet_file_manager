import flet as ft
import shutil

from router.FletRouter import FletRouter
from router.RouterBody import RouterBody

from layout.LayoutTop import LayoutTop
from layout.LayoutBottom import LayoutBottom
from AppContext import AppContext
from events.AppEvents import AppEvents


def main(page: ft.Page):
    app = AppContext(page, FletRouter(page), AppEvents())
    routerBody = RouterBody(app)

    page.on_route_change = routerBody.route_change
    page.go(".")
    
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.add(LayoutTop(app).control)
    page.add(routerBody.body)
    page.add(LayoutBottom(app).control)


ft.app(main)
