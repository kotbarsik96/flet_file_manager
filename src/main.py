# libs
import flet as ft
from pathlib import Path

# core
from Core import System
from Events import AppEvents
from Router import Router

# view
from view.layout.LayoutMenuBar import LayoutMenuBar
from view.layout.LayoutTop import LayoutTop
from view.layout.LayoutBottom import LayoutBottom


def main(page: ft.Page):
    system = System(Path.cwd())
    events = AppEvents()
    router = Router(page=page, events=events, system=system)

    page.on_route_change = router.on_route_change
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    layoutMenuBar = LayoutMenuBar(page=page)
    layoutTop = LayoutTop(page=page, router=router, events=events)
    layoutBottom = LayoutBottom(page=page, router=router, system=system)

    page.add(ft.Row([layoutMenuBar.view]))
    page.add(layoutTop.view)
    page.add(router.body)
    page.add(layoutBottom.view)
    
    page.go(str(system.root_path))


ft.app(main)
