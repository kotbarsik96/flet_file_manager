import flet as ft
from pathlib import Path
from utils.file_system import format_bytes_to_string, get_dir_size
from utils.time import format_seconds, format_date, SetInterval
import time
from view.BaseView import BaseView
from Core import System
from Events import AppEvents


class FolderView(BaseView):

    def __init__(
        self,
        page: ft.Page,
        system: System,
        events: AppEvents,
        go_prev_route: callable,
        go_next_route: callable,
    ):
        self.page = page
        self.system = system
        self.keyboard_controller = FolderViewKeyboardController(events=events, go_prev_route=go_prev_route, go_next_route=go_next_route)
        self.build_view()

    def route_to_path(self):
        return str(Path(self.page.route).absolute())

    def build_view(self):
        path = self.route_to_path()
        it = Path(path)
        if not it.exists():
            it = Path(self.system.root_path)
            dlg = ft.AlertDialog(
                title=ft.Text(f'Указанный путь "{path}" не существует')
            )
            self.page.open(dlg)

        columns = [
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Тип")),
            ft.DataColumn(ft.Text("Дата изменения")),
            ft.DataColumn(ft.Text("Вес")),
        ]
        rows = list(
            map(
                self.create_row,
                it.iterdir(),
            )
        )
        self.keyboard_controller.rows = rows

        self.view = ft.ResponsiveRow(
            [
                ft.DataTable(
                    columns=columns, rows=rows, width=750, col={"xs": 12, "xl": 8}
                ),
                self.create_timers(),
            ],
            columns=12,
            spacing=20,
        )

    def create_row(self, item: Path):
        # тип: папка или расширение файла
        extension = "Папка" if item.is_dir() else "Файл ." + item.name.split(".")[-1]
        # размер
        stat = item.stat()
        size = (
            format_bytes_to_string(stat.st_size)
            if item.is_file()
            else format_bytes_to_string(get_dir_size(str(item.absolute())))
        )
        # время последнего обновления
        updated = format_date(stat.st_mtime)

        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item.name)),
                ft.DataCell(ft.Text(extension)),
                ft.DataCell(ft.Text(updated)),
                ft.DataCell(ft.Text(size)),
            ],
        )

        if item.is_dir():
            row.on_select_changed = lambda _: self.page.go(str(item.absolute()))

        return row

    def create_timers(self):
        font_size = 18

        os_session_timer_text = ft.Text(
            format_seconds(time.monotonic()), size=font_size
        )
        app_session_timer_text = ft.Text(
            format_seconds(self.system.app_running_seconds), size=font_size
        )

        def update_timers():
            os_session_timer_text.value = format_seconds(time.monotonic())
            app_session_timer_text.value = format_seconds(
                self.system.app_running_seconds
            )
            self.page.update()

        SetInterval(update_timers, 1)

        os_session_timer_control = ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Время работы операционной системы:", size=font_size),
                        os_session_timer_text,
                    ]
                ),
                ft.Column(
                    [
                        ft.Text("Время работы приложения:", size=font_size),
                        app_session_timer_text,
                    ]
                ),
            ]
        )

        return ft.Column([os_session_timer_control], col={"xs": 12, "xl": 4})


class FolderViewKeyboardController:
    rows: list[ft.DataRow]
    current_selected_index: int | None

    def __init__(self, events: AppEvents, go_prev_route: callable, go_next_route: callable):
        self.go_prev_route = go_prev_route
        self.go_next_route = go_next_route
        self.current_selected_index = None
        self.rows = []

        events.keyboard.subscribe(self.handle_keyboard)

    def update_rows(self, rows):
        self.rows = rows

    def handle_keyboard(self, event: ft.KeyboardEvent):
        if event.key == "Arrow Left" and event.ctrl:
            self.handle_arrow_left(event)
        if event.key == "Arrow Right" and event.ctrl:
            self.handle_arrow_right(event)

    def handle_arrow_left(self, event: ft.KeyboardEvent):
        self.go_prev_route()

    def handle_arrow_right(self, event: ft.KeyboardEvent):
        self.go_next_route()
