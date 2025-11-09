import flet as ft
from view.BaseView import BaseView
import subprocess
import shutil
from Core import System
from ui.dialogs.MenuBarDialogs import (
    AppTimeDialog,
    HelpDialog,
    OSTimeDialog,
    HotkeysDialog,
)


class LayoutMenuBar(BaseView):
    def __init__(self, page: ft.Page, system: System):
        self.page = page
        self.system = system

        self.build_view()

    def build_view(self):
        self.view = ft.MenuBar(
            expand=True,
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("Файл"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("Открыть терминал"),
                            leading=ft.Icon(ft.Icons.TERMINAL),
                            on_click=self.on_terminal_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Время работы системы"),
                            leading=ft.Icon(ft.Icons.COMPUTER),
                            on_click=self.on_os_time_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Время работы приложения"),
                            leading=ft.Icon(ft.Icons.TIMER),
                            on_click=self.on_app_time_click,
                        ),
                    ],
                ),
                ft.SubmenuButton(
                    content=ft.Text("Помощь"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("О программе"),
                            leading=ft.Icon(ft.Icons.INFO),
                            on_click=self.on_help_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Горячие клавиши"),
                            leading=ft.Icon(ft.Icons.KEYBOARD),
                            on_click=self.on_hotkeys_click,
                        ),
                    ],
                ),
            ],
        )

    def on_help_click(self, e):
        HelpDialog(page=self.page)

    def on_hotkeys_click(self, e):
        HotkeysDialog(page=self.page)

    def on_terminal_click(self, e):
        msg = "Терминал открыт через файловый менеджер"

        if shutil.which("gnome-terminal"):
            return subprocess.Popen(
                [
                    "gnome-terminal",
                    "--",
                    "bash",
                    "-c",
                    f"echo '{msg}'; exec bash",
                ]
            )
        elif shutil.which("xterm"):
            return subprocess.Popen(
                ["xterm", "-e", f"bash -lc echo '${msg}'; exec bash"]
            )
        else:
            error_msg = "Не найден установленный терминал"
            self.open_info_dialog(
                title=ft.Text("Ошибка"),
                content=ft.Text(error_msg, size=18),
            )
            raise RuntimeError(error_msg)

    def on_os_time_click(self, e):
        OSTimeDialog(self.page)

    def on_app_time_click(self, e):
        AppTimeDialog(self.page, self.system)
