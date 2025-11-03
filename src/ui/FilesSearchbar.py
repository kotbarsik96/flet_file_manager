import flet as ft

from pathlib import Path
from AppContext import AppContext


class FilesSearchbar:
    def __init__(self, app: AppContext, col: dict[str, int] | int | None = None):
        self.app = app
        self.listView = ft.ListView(controls=[])
        self.control = ft.SearchBar(
            on_change=self.handle_change,
            on_tap=self.handle_tap,
            controls=[self.listView],
            bar_hint_text="Поиск во вложенных каталогах...",
            view_hint_text="Название файла или папки",
            col=col
        )

    def handle_change(self, e: ft.ControlEvent):
        search_value = e.data
        self.listView.controls.clear()

        if search_value.strip():
            current_dir = Path(self.app.router.current_route)
            rglob = current_dir.rglob(search_value)

            def on_item_click(path: str):
                self.app.page.go(path)
                self.control.close_view(search_value)

            for entry in rglob:
                self.listView.controls.append(
                    ft.ListTile(
                        title=ft.Text(entry.name),
                        subtitle=ft.Text(str(entry.absolute())),
                        on_click=lambda _, iteration_entry=entry: on_item_click(
                            str(iteration_entry.absolute())
                        ),
                    )
                )

        self.app.page.update()

    def handle_tap(self, e: ft.ControlEvent):
        self.control.open_view()
