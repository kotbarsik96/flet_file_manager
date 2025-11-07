import flet as ft
import shutil

from pathlib import Path
from view.BaseView import BaseView
from Core import System
from Router import Router
from utils.file_system import format_bytes_to_string


class LayoutBottom(BaseView):
    def __init__(self, page: ft.Page, system: System, router: Router):
        self.page = page
        self.system = system
        self.router = router
        
        self.build_view()
    
    def build_view(self):
        path = (
            str(Path(self.router.current_route).absolute())
            if self.router.current_route
            else "."
        )
        total, used, free = shutil.disk_usage(path)
        total_one_percent = total / 100

        used_percent = used / (total_one_percent)
        free_percent = free / (total_one_percent)

        container_width = 1000
        bar_height = 5

        self.view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Пространство текущего раздела диска:", size=21, weight=700
                        )
                    ]
                ),
                ft.Container(
                    width=container_width,
                    content=ft.Row(
                        [
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"Используется: {round(used_percent)}% ({format_bytes_to_string(round(used))})"
                                    ),
                                    ft.Container(
                                        width=container_width / 100 * used_percent,
                                        height=bar_height,
                                        bgcolor=ft.Colors.RED,
                                    ),
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"Свободно: {round(free_percent)}% ({format_bytes_to_string(round(free))})"
                                    ),
                                    ft.Container(
                                        width=container_width / 100 * free_percent,
                                        height=bar_height,
                                        bgcolor=ft.Colors.GREEN,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ),
            ],
            spacing=15,
        )
