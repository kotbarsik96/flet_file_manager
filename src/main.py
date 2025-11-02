import flet as ft
import time

from router.FletRouter import FletRouter
from router.RouterBody import RouterBody

from layout.LayoutTop import LayoutTop
from layout.LayoutBottom import LayoutBottom
from AppContext import AppContext
from events.AppEvents import AppEvents
from mediaQuery.MediaQueryManager import MediaQueryManager


def main(page: ft.Page):
    app = AppContext(page, FletRouter(page), AppEvents(), MediaQueryManager())
    routerBody = RouterBody(app)
    page.on_resized = app.media_query_manager.on_resized

    page.on_route_change = routerBody.route_change
    page.go(".")

    page.scroll = ft.ScrollMode.ADAPTIVE

    page.add(LayoutTop(app).layout)
    page.add(routerBody.body)
    page.add(LayoutBottom(app).layout)


ft.app(main)
