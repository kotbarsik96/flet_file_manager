import flet as ft
from view.BaseView import BaseView
import subprocess
import shutil
from view.layout.blocks.TimerBlocks import TimerOS, TimerApp
from Core import System


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

    def open_info_dialog(self, title, content):
        dlg = ft.AlertDialog(
            title=title,
            content=content,
            actions=[ft.TextButton("Закрыть", on_click=lambda e: self.page.close(dlg))],
        )
        self.page.open(dlg)
        return dlg

    def on_help_click(self, e):
        paragraphs = [
            "Файловый менеджер на языке Python с использованием Flet",
            "Разработчик: Никифоров Алексей Владимирович",
            "Группа: ИВТз-43у",
        ]

        content = ft.Column(controls=[])
        for paragraph in paragraphs:
            content.controls.append(ft.Text(paragraph, size=18))

        self.open_info_dialog(
            title=ft.Text("О программе"),
            content=content,
        )

    def on_hotkeys_click(self, e):
        paragraphs = [
            "– Стрелки вверх-вниз: навигация по доступным кнопкам в приложении",
            "– Стрелка вправо при выделенном элементе - открыть папку/файл (если поддерживается)",
            "– CTRL + Стрелка влево: перейти на предыдущую страницу",
            "– CTRL + Стрелка вправо: перейти на следующую страницу",
        ]

        content = ft.Column(controls=[])
        for paragraph in paragraphs:
            content.controls.append(ft.Text(paragraph, size=18))

        self.open_info_dialog(title=ft.Text("Горячие клавиши"), content=content)

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
        timer = TimerOS(self.page)
        dlg = self.open_info_dialog("Время работы системы", timer.timer_text)
        dlg.on_dismiss = timer.on_onmount

    def on_app_time_click(self, e):
        timer = TimerApp(self.page, self.system)
        dlg = self.open_info_dialog("Время работы приложения", timer.timer_text)
        dlg.on_dismiss = timer.on_onmount
