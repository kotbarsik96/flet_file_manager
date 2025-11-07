import flet as ft
from view.BaseView import BaseView


class LayoutMenuBar(BaseView):
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.build_view()

    def build_view(self):
        self.view = ft.MenuBar(
            expand=True,
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("Помощь"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("О программе"),
                            leading=ft.Icon(ft.Icons.INFO),
                            on_click=self.on_help_click
                        )
                    ],
                )
            ],
        )
        
    def on_help_click(self, e):
        font_size = 18
        dlg = ft.AlertDialog(
            title=ft.Text("О программе"),
            content=ft.Column([
                ft.Text("Файловый менеджер на языке Python с использованием Flet", size=font_size),
                ft.Text("Разработчик: Никифоров Алексей Владимирович", size=font_size),
                ft.Text("Группа: ИВТз-43у", size=font_size),
            ]),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: self.page.close(dlg))
            ]
        )
        self.page.open(dlg)
