import flet as ft
from pathlib import Path
from utils.file_system import format_bytes_to_string, get_dir_size
from utils.time import format_seconds, format_date, SetInterval
import time
from view.BaseView import BaseView
from Core import System
from Events import AppEvents


class FolderColumns:
    def __init__(self):
        self.columns_list = [
            ft.Container(
                ft.Text("Название", size=folderViewStyles.font_size),
                col=1,
                border=ft.border.only(
                    top=folderViewStyles.table_border,
                    right=folderViewStyles.table_border,
                    bottom=folderViewStyles.table_border,
                ),
                padding=folderViewStyles.cell_padding,
            ),
            ft.Container(
                ft.Text("Тип", size=folderViewStyles.font_size),
                col=1,
                border=ft.border.only(
                    top=folderViewStyles.table_border,
                    right=folderViewStyles.table_border,
                    bottom=folderViewStyles.table_border,
                ),
                padding=folderViewStyles.cell_padding,
            ),
            ft.Container(
                ft.Text("Дата изменения", size=folderViewStyles.font_size),
                col=1,
                border=ft.border.only(
                    top=folderViewStyles.table_border,
                    right=folderViewStyles.table_border,
                    bottom=folderViewStyles.table_border,
                ),
                padding=folderViewStyles.cell_padding,
            ),
            ft.Container(
                ft.Text("Вес", size=folderViewStyles.font_size),
                col=1,
                border=ft.border.only(
                    top=folderViewStyles.table_border,
                    bottom=folderViewStyles.table_border,
                ),
                padding=folderViewStyles.cell_padding,
            ),
        ]
        self.cols_count = len(self.columns_list)
        self.columns_view = ft.ResponsiveRow(
            self.columns_list, columns=self.cols_count, spacing=0
        )


class FolderRowItem:
    row: ft.ResponsiveRow
    row_container: ft.Container

    def __init__(self, path: Path, cols_count: int):
        self.path = path

        # тип: папка или расширение файла
        self.extension = (
            "Папка" if path.is_dir() else "Файл ." + path.name.split(".")[-1]
        )
        # размер
        self.stat = path.stat()
        self.size = (
            format_bytes_to_string(self.stat.st_size)
            if path.is_file()
            else format_bytes_to_string(get_dir_size(str(path.absolute())))
        )
        # время последнего обновления
        self.updated = format_date(self.stat.st_mtime)

        self.row_container = ft.Container(
            ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text(path.name, size=folderViewStyles.font_size),
                        col=1,
                        border=ft.border.only(
                            right=folderViewStyles.table_border,
                            bottom=folderViewStyles.table_border,
                        ),
                        padding=folderViewStyles.cell_padding,
                    ),
                    ft.Container(
                        ft.Text(self.extension, size=folderViewStyles.font_size),
                        col=1,
                        border=ft.border.only(
                            right=folderViewStyles.table_border,
                            bottom=folderViewStyles.table_border,
                        ),
                        padding=folderViewStyles.cell_padding,
                    ),
                    ft.Container(
                        ft.Text(self.updated, size=folderViewStyles.font_size),
                        col=1,
                        border=ft.border.only(
                            right=folderViewStyles.table_border,
                            bottom=folderViewStyles.table_border,
                        ),
                        padding=folderViewStyles.cell_padding,
                    ),
                    ft.Container(
                        ft.Text(self.size, size=folderViewStyles.font_size),
                        col=1,
                        border=ft.border.only(bottom=folderViewStyles.table_border),
                        padding=folderViewStyles.cell_padding,
                    ),
                ],
                columns=cols_count,
                spacing=0,
            ),
            on_click=lambda e: self.on_row_click(event=e),
        )

        self.row = ft.ResponsiveRow(
            [self.row_container],
        )

        self._isSelected = False

    def get_selected_state(self) -> bool:
        return self._isSelected

    def set_selected_state(self, _isSelected: bool):
        self._isSelected = _isSelected

        if self._isSelected:
            pass
        else:
            pass

    def on_row_click(self, event):
        if self.path.is_dir():
            self.page.go(str(self.path.absolute()))

    def handle_delete(self):
        print(self.path)


class FolderView(BaseView):
    row_items: list[FolderRowItem]
    selected_row_container_index: None | int

    def __init__(self, page: ft.Page, system: System, events: AppEvents):
        self.page = page
        self.system = system
        self.events = events
        self.row_items = []
        self.selected_row_container_index = None
        self.path = Path(self.page.route)

        self.build_view()
        events.keyboard.subscribe(self.handle_keyboard)

    def build_view(self):
        if not self.path.exists():
            dlg = ft.AlertDialog(
                title=ft.Text(f'Указанный путь "{self.path.resolve()}" не существует')
            )
            self.path = Path(self.system.root_path)
            self.page.open(dlg)

        self.columns_data = FolderColumns()

        self.row_items = [
            FolderRowItem(path=path, cols_count=self.columns_data.cols_count)
            for path in self.path.iterdir()
        ]

        view_content = [self.columns_data.columns_view]
        view_content.extend([row_item.row for row_item in self.row_items])
        view_content.extend([self.create_timers()])

        self.view = ft.Column(view_content, spacing=0)

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
        for row_item in [
            row_item for row_item in self.row_items if row_item.get_selected_state()
        ]:
            row_item.handle_delete()

    def handle_arrow_up_or_down(self, event, direction: str):
        rows_len = len(self.row_items)

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

        for idx, row_item in enumerate(self.row_items):
            if idx == self.selected_row_container_index:
                row_item.set_selected_state(True)
            else:
                row_item.set_selected_state(False)


class FolderViewStyles:
    def __init__(self):
        self.table_border = ft.border.BorderSide(1, "black")
        self.font_size = 18
        self.cell_padding = ft.padding.only(right=15, left=15, top=10, bottom=10)


folderViewStyles = FolderViewStyles()
