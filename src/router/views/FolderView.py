import flet as ft, datetime
from pathlib import Path
from router.views.BaseView import BaseView
from utils.file_system import format_bytes_to_string, get_dir_size
from utils.time import format_seconds, SetInterval
import time


class FolderView(BaseView):
    default_path = "."

    def route_to_path(self):
        return str(Path(self.app.page.route).absolute())

    def build_view(self):
        path = self.route_to_path()
        it = Path(path)
        if not it.exists():
            it = Path(self.default_path)
            dlg = ft.AlertDialog(
                title=ft.Text(f'Указанный путь "{path}" не существует')
            )
            self.app.page.open(dlg)

        columns = [
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Тип")),
            ft.DataColumn(ft.Text("Дата создания")),
            ft.DataColumn(ft.Text("Дата изменения")),
            ft.DataColumn(ft.Text("Вес")),
        ]
        rows = list(
            map(
                self.map_scandir,
                it.iterdir(),
            )
        )

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

    def map_scandir(self, item: Path):
        extension = "Папка" if item.is_dir() else "Файл ." + item.name.split(".")[-1]
        stat = item.stat()
        size = (
            format_bytes_to_string(stat.st_size)
            if item.is_file()
            else format_bytes_to_string(get_dir_size(str(item.absolute())))
        )

        formatDatetime = "%d.%m.%Y, %H:%M:%S"
        created = datetime.datetime.fromtimestamp(stat.st_birthtime).strftime(
            formatDatetime
        )
        updated = datetime.datetime.fromtimestamp(stat.st_mtime).strftime(
            formatDatetime
        )
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item.name)),
                ft.DataCell(ft.Text(extension)),
                ft.DataCell(ft.Text(created)),
                ft.DataCell(ft.Text(updated)),
                ft.DataCell(ft.Text(size)),
            ],
        )

        if item.is_dir():
            row.on_select_changed = lambda _: self.app.page.go(str(item.absolute()))

        return row

    def create_timers(self):
        os_session_timer_text = ft.Text(format_seconds(time.monotonic()), size=18)
        app_session_timer_text = ft.Text(
            format_seconds(self.app.app_running_seconds), size=18
        )

        def update_timers():
            os_session_timer_text.value = format_seconds(time.monotonic())
            app_session_timer_text.value = format_seconds(self.app.app_running_seconds)
            self.app.page.update()

        SetInterval(update_timers, 1)

        os_session_timer_control = ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Время работы операционной системы:", size=18),
                        os_session_timer_text,
                    ]
                ),
                ft.Column(
                    [
                        ft.Text("Время работы приложения:", size=18),
                        app_session_timer_text,
                    ]
                ),
            ]
        )

        return ft.Column([os_session_timer_control], col={"xs": 12, "xl": 4})
