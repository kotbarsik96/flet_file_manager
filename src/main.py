# libs
import flet as ft
from pathlib import Path
import time

# core
from Core import System
from Events import AppEvents
from Router import Router
from GlobalKeyboardHandler import GlobalKeyboardHandler

# view
from view.layout.LayoutMenuBar import LayoutMenuBar
from view.layout.LayoutTop import LayoutTop
from view.layout.blocks.SpaceStatsBlock import SpaceStatsBlock

# utils
from utils.time import format_date


def main(page: ft.Page):
    page.title = "PSUTI File Manager"
    
    system = System(Path.cwd())
    events = AppEvents(system=system)
    router = Router(page=page, events=events, system=system)
    
    page.bgcolor=ft.Colors.GREY_100

    page.on_route_change = router.on_route_change
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.on_keyboard_event = lambda e: events.keyboard.trigger(e)

    GlobalKeyboardHandler(system=system, events=events, page=page, router=router)

    # events.keyboard.subscribe(lambda e: print(e)) # debug событий клавиатуры

    layoutMenuBar = LayoutMenuBar(
        page=page, system=system, router=router, events=events
    )
    layoutTop = LayoutTop(page=page, router=router, events=events, system=system)

    page.add(ft.Row([layoutMenuBar.view]))
    page.add(layoutTop.view)
    page.add(router.body)

    page.go(str(system.root_path))
    system.logger.write_log(f"Программа открыта | {format_date(time.time())}")


ft.app(main)
