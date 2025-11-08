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
        events: AppEvents
    ):
        self.page = page
        self.system = system
        self.events = events
        
        self.build_view()
        events.keyboard.subscribe(self.handle_keyboard)

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

        self.columns = [
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Тип")),
            ft.DataColumn(ft.Text("Дата изменения")),
            ft.DataColumn(ft.Text("Вес")),
        ]
        self.rows = list(
            map(
                self.create_row,
                it.iterdir(),
            )
        )

        self.view = ft.ResponsiveRow(
            [
                ft.DataTable(
                    columns=self.columns, rows=self.rows, width=750, col={"xs": 12, "xl": 8}
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
            row.on_select_changed = lambda e: print(e)

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

    def handle_keyboard(self, event: ft.KeyboardEvent):
        if event.key == 'Delete':
            self.handle_delete(event)
            
    def handle_delete(self, event: ft.KeyboardEvent):
        print(event)
        selected_rows = [row for row in self.rows if row.selected]
        print(selected_rows)