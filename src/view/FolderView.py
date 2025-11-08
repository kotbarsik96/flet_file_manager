import flet as ft
from pathlib import Path
from utils.file_system import format_bytes_to_string, get_dir_size
from utils.time import format_seconds, format_date, SetInterval
import time
from view.BaseView import BaseView
from Core import System
from Events import AppEvents


class FolderView(BaseView):
    row_containers = list[ft.Container]
    selected_row_container_index: None | int

    def __init__(self, page: ft.Page, system: System, events: AppEvents):
        self.page = page
        self.system = system
        self.events = events
        self.row_containers = []
        self.selected_row_container_index = None

        self.styles = FolderViewStyles()

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
            ft.Container(
                ft.Text("Название", size=self.styles.font_size),
                col=1,
                border=ft.border.only(
                    top=self.styles.table_border,
                    right=self.styles.table_border,
                    bottom=self.styles.table_border,
                ),
                padding=self.styles.cell_padding,
            ),
            ft.Container(
                ft.Text("Тип", size=self.styles.font_size),
                col=1,
                border=ft.border.only(
                    top=self.styles.table_border,
                    right=self.styles.table_border,
                    bottom=self.styles.table_border,
                ),
                padding=self.styles.cell_padding,
            ),
            ft.Container(
                ft.Text("Дата изменения", size=self.styles.font_size),
                col=1,
                border=ft.border.only(
                    top=self.styles.table_border,
                    right=self.styles.table_border,
                    bottom=self.styles.table_border,
                ),
                padding=self.styles.cell_padding,
            ),
            ft.Container(
                ft.Text("Вес", size=self.styles.font_size),
                col=1,
                border=ft.border.only(
                    top=self.styles.table_border, bottom=self.styles.table_border
                ),
                padding=self.styles.cell_padding,
            ),
        ]
        cols_count = len(self.columns)

        self.rows = list(
            map(
                lambda item: self.create_row(item=item, cols_count=cols_count),
                it.iterdir(),
            )
        )

        view_content = [ft.ResponsiveRow(self.columns, columns=cols_count, spacing=0)]
        view_content.extend(self.rows)
        view_content.extend([self.create_timers()])

        self.view = ft.Column(view_content, spacing=0)

    def create_row(self, item: Path, cols_count: int):
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

        row_container = ft.Container(
            ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text(item.name, size=self.styles.font_size),
                        col=1,
                        border=ft.border.only(
                            right=self.styles.table_border,
                            bottom=self.styles.table_border,
                        ),
                        padding=self.styles.cell_padding,
                    ),
                    ft.Container(
                        ft.Text(extension, size=self.styles.font_size),
                        col=1,
                        border=ft.border.only(
                            right=self.styles.table_border,
                            bottom=self.styles.table_border,
                        ),
                        padding=self.styles.cell_padding,
                    ),
                    ft.Container(
                        ft.Text(updated, size=self.styles.font_size),
                        col=1,
                        border=ft.border.only(
                            right=self.styles.table_border,
                            bottom=self.styles.table_border,
                        ),
                        padding=self.styles.cell_padding,
                    ),
                    ft.Container(
                        ft.Text(size, size=self.styles.font_size),
                        col=1,
                        border=ft.border.only(bottom=self.styles.table_border),
                        padding=self.styles.cell_padding,
                    ),
                ],
                columns=cols_count,
                spacing=0,
            ),
            on_click=lambda e: self.on_row_click(event=e, item=item),
        )

        row = ft.ResponsiveRow(
            [row_container],
        )

        row_container.data = {"selected": False}

        self.row_containers.append(row_container)

        return row

    def on_row_click(self, event, item: Path):
        if item.is_dir():
            self.page.go(str(item.absolute()))

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
        if event.key == "Delete":
            self.handle_delete(event)

        if event.key == "Arrow Up":
            self.handle_arrow_up_or_down(event, direction="up")

        if event.key == "Arrow Down":
            self.handle_arrow_up_or_down(event, direction="down")

    def handle_delete(self, event: ft.KeyboardEvent):
        selected_rows = [row_container for row_container in self.row_containers if row_container.data["selected"]]

    def handle_arrow_up_or_down(self, event, direction: str):
        rows_len = len(self.row_containers)

        if (
            not self.selected_row_container_index
            and self.selected_row_container_index != 0
        ):
            self.selected_row_container_index = 0
        elif direction == "up":
            self.selected_row_container_index -= 1
        elif direction == "down":
            self.selected_row_container_index += 1

        if (
            self.selected_row_container_index < 0
            or self.selected_row_container_index >= rows_len
        ):
            if direction == "up":
                self.selected_row_container_index = rows_len - 1
            elif direction == "down":
                self.selected_row_container_index = 0

        self.select_row_container(self.selected_row_container_index)
        print(self.selected_row_container_index)

    def select_row_container(self, index):
        rows_len = len(self.row_containers)

        if 0 <= index < rows_len:
            for idx, row_container in enumerate(self.row_containers):
                if idx == index:
                    row_container.data["selected"] = True
                else:
                    row_container.data["selected"] = False


class FolderViewStyles:
    def __init__(self):
        self.table_border = ft.border.BorderSide(1, "black")
        self.font_size = 18
        self.cell_padding = ft.padding.only(right=15, left=15, top=10, bottom=10)
