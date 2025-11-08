import flet as ft
from view.BaseView import BaseView
import subprocess
import shutil


class LayoutMenuBar(BaseView):
    def __init__(self, page: ft.Page):
        self.page = page

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
                        )
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

    def on_help_click(self, e):
        font_size = 18
        self.open_info_dialog(
            title=ft.Text("О программе"),
            content=ft.Column(
                [
                    ft.Text(
                        "Файловый менеджер на языке Python с использованием Flet",
                        size=font_size,
                    ),
                    ft.Text(
                        "Разработчик: Никифоров Алексей Владимирович", size=font_size
                    ),
                    ft.Text("Группа: ИВТз-43у", size=font_size),
                ]
            ),
        )

    def on_hotkeys_click(self, e):
        font_size = 18

        self.open_info_dialog(
            title=ft.Text("Горячие клавиши"),
            content=ft.Column(
                [
                    ft.Text(
                        "– Стрелки вверх-вниз: навигация по доступным кнопкам в приложении",
                        size=font_size,
                    ),
                    ft.Text(
                        "– CTRL + Стрелка влево: перейти на предыдущую страницу",
                        size=font_size,
                    ),
                    ft.Text(
                        "– CTRL + Стрелка вправо: перейти на следующую страницу",
                        size=font_size,
                    ),
                ]
            ),
        )

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
