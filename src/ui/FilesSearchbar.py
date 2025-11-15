import flet as ft, os, re
from pathlib import Path
from Router import Router


class FilesSearchbar:
    def __init__(
        self, page: ft.Page, router: Router, col: dict[str, int] | int | None = None
    ):
        self.page = page
        self.router = router
        self.listView = ft.ListView(controls=[])
        self.control = ft.SearchBar(
            on_change=self.handle_change,
            on_tap=self.handle_tap,
            controls=[self.listView],
            bar_hint_text="Поиск во вложенных каталогах...",
            view_hint_text="Название файла или папки",
            col=col,
        )

    def handle_change(self, e: ft.ControlEvent):
        self.search_value = e.data.lower()
        escaped_value = re.escape(self.search_value)
        self.listView.controls.clear()

        stripped = self.search_value.strip()
        if stripped and len(stripped) >= 3:
            current_dir = Path(self.router.current_route)
            results_limit = 5
            results_count = 0
            for root, dirs, files in os.walk(current_dir):
                _root = "" if root == "/" else root
                if results_count >= results_limit:
                    break

                for dir_name in dirs:
                    if re.search(escaped_value, dir_name.lower()):
                        results_count += 1
                        self.append_found_entity(Path(f"{_root}/{dir_name}"))

                for file_name in files:
                    if re.search(escaped_value, file_name.lower()):
                        results_count += 1
                        self.append_found_entity(Path(f"{_root}/{file_name}"))

        self.page.update()

    def append_found_entity(self, path: Path):
        self.listView.controls.append(
            ft.ListTile(
                title=ft.Text(path.name),
                subtitle=ft.Text(str(path.absolute())),
                on_click=lambda _: self.on_item_click(path),
            )
        )

    def handle_tap(self, e: ft.ControlEvent):
        self.control.open_view()

    def on_item_click(self, path: Path):
        if path.is_dir():
            self.page.go(str(path.absolute()))
        else:
            self.page.go(str(path.parent.absolute()))

        self.control.close_view(self.search_value)
