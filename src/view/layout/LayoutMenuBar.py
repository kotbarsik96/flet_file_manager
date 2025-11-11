import flet as ft
from view.BaseView import BaseView
from Core import System
from Events import AppEvents
from Router import Router
from ui.dialogs.MenuBarDialogs import (
    AppTimeDialog,
    HelpDialog,
    OSTimeDialog,
    HotkeysDialog,
    SpaceStatsDialog,
)
from utils.general import open_os_terminal


class LayoutMenuBar(BaseView):
    def __init__(
        self, page: ft.Page, system: System, events: AppEvents, router: Router
    ):
        self.page = page
        self.system = system
        self.events = events
        self.router = router

        self.on_mounted()

    def on_mounted(self):
        self.build_view()

    def on_unmount(self):
        pass

    def build_view(self):
        self.view = ft.MenuBar(
            expand=True,
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("Файл"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("Статистика текущего раздела диска (F5)"),
                            leading=ft.Icon(ft.Icons.INCOMPLETE_CIRCLE_ROUNDED),
                            on_click=lambda _: SpaceStatsDialog(
                                self.page, self.system, self.router
                            ),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Открыть терминал (встроенный) (F6)"),
                            leading=ft.Icon(ft.Icons.TERMINAL_OUTLINED),
                            on_click=self.on_terminal_embed_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text(
                                "Открыть терминал (внешний, ОС) (CTRL + F6)"
                            ),
                            leading=ft.Icon(ft.Icons.TERMINAL),
                            on_click=lambda _: open_os_terminal(
                                page=self.page, router=self.router
                            ),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Время работы системы (F7)"),
                            leading=ft.Icon(ft.Icons.COMPUTER),
                            on_click=lambda _: OSTimeDialog(self.page),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Время работы приложения (CTRL + F7)"),
                            leading=ft.Icon(ft.Icons.TIMER),
                            on_click=lambda _: AppTimeDialog(self.page, self.system),
                        ),
                    ],
                ),
                ft.SubmenuButton(
                    content=ft.Text("Помощь"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("О программе"),
                            leading=ft.Icon(ft.Icons.INFO),
                            on_click=lambda _: HelpDialog(page=self.page),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Горячие клавиши"),
                            leading=ft.Icon(ft.Icons.KEYBOARD),
                            on_click=lambda _: HotkeysDialog(page=self.page),
                        ),
                    ],
                ),
            ],
        )

    def on_terminal_embed_click(self, e):
        self.page.go("__Terminal__")
