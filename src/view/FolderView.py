import flet as ft
from pathlib import Path
from utils.file_system import format_bytes_to_string, get_dir_size
from utils.time import format_date
from view.BaseView import BaseView
from Core import System
from Events import AppEvents
import shutil


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

    def __init__(self, path: Path, cols_count: int, page: ft.Page, system: System):
        self.page = page
        self.path = path
        self.system = system

        self.name_row = ft.Container(
            ft.Text("", size=folderViewStyles.font_size),
            col=1,
            border=ft.border.only(
                right=folderViewStyles.table_border,
                bottom=folderViewStyles.table_border,
            ),
            padding=folderViewStyles.cell_padding,
        )
        self.extension_row = ft.Container(
            ft.Text("", size=folderViewStyles.font_size),
            col=1,
            border=ft.border.only(
                right=folderViewStyles.table_border,
                bottom=folderViewStyles.table_border,
            ),
            padding=folderViewStyles.cell_padding,
        )
        self.updated_row = ft.Container(
            ft.Text("", size=folderViewStyles.font_size),
            col=1,
            border=ft.border.only(
                right=folderViewStyles.table_border,
                bottom=folderViewStyles.table_border,
            ),
            padding=folderViewStyles.cell_padding,
        )
        self.size_row = ft.Container(
            ft.Text("", size=folderViewStyles.font_size),
            col=1,
            border=ft.border.only(bottom=folderViewStyles.table_border),
            padding=folderViewStyles.cell_padding,
        )

        self.update_data()

        self.row_container = ft.Container(
            ft.ResponsiveRow(
                [
                    self.name_row,
                    self.extension_row,
                    self.updated_row,
                    self.size_row,
                ],
                columns=cols_count,
                spacing=0,
            ),
            on_click=lambda e: self.on_row_click(event=e),
            on_long_press=lambda e: self.on_long_press(event=e),
            on_hover=self.on_hover,
            bgcolor=folderViewStyles.row_container_bg_color,
        )

        self.row = ft.ResponsiveRow(
            [self.row_container],
        )

        self._isSelected = False

    def update_data(self):
        # тип: папка или расширение файла
        if self.path.is_dir():
            self.extension = "Папка"
        else:
            split = self.path.name.split(".")
            has_extension = len(split) > 1
            self.extension = (
                f"Файл {"." + split[-1] if has_extension else "без расширения"}"
            )
        # размер
        self.stat = self.path.stat()
        self.size = (
            format_bytes_to_string(self.stat.st_size)
            if self.path.is_file()
            else format_bytes_to_string(get_dir_size(str(self.path.absolute())))
        )
        # время последнего обновления
        self.updated = format_date(self.stat.st_mtime)

        self.name_row.content.value = self.path.name
        self.extension_row.content.value = self.extension
        self.size_row.content.value = self.size
        self.updated_row.content.value = self.updated

    def can_be_deleted_or_renamed(self, modal_on_failure: bool = False):
        resolved_path = self.path.resolve()
        # файл может быть удалён если он находится в корзине или не в папке system
        can_be = self.is_in_trash() or not resolved_path.is_relative_to(
            self.system.system_path
        )

        if not can_be and modal_on_failure:
            text = (
                "Данная папка не может быть удалена/переименована"
                if self.path.is_dir()
                else "Данный файл не может быть удалён/переименован"
            )
            dlg = ft.AlertDialog(
                title=ft.Text("Ошибка"),
                content=ft.Text(text),
                actions=[
                    ft.TextButton("Закрыть", on_click=lambda _: self.page.close(dlg))
                ],
            )
            self.page.open(dlg)

        return can_be

    def is_in_trash(self):
        resolved_path = self.path.resolve()
        return resolved_path.is_relative_to(self.system.trash.path) and resolved_path != self.system.trash.path

    def get_selected_state(self) -> bool:
        return self._isSelected

    def set_selected_state(self, _isSelected: bool):
        self._isSelected = _isSelected

        if self._isSelected:
            self.row_container.bgcolor = (
                folderViewStyles.row_container_bg_color_selected
            )
        else:
            self.row_container.bgcolor = folderViewStyles.row_container_bg_color

        self.page.update()

    def on_hover(self, event: ft.HoverEvent):
        # когда курсор наведён
        if event.data == "true":
            self.row_container.bgcolor = folderViewStyles.row_container_bg_color_hovered
        # когда курсор убран
        else:
            self.row_container.bgcolor = folderViewStyles.row_container_bg_color

        self.page.update()

    def on_row_click(self, event):
        if self.path.is_dir():
            self.page.go(str(self.path.absolute()))

    def on_long_press(self, event):
        delete_action = ft.TextButton(
            "Переместить в корзину",
            on_click=lambda _: self.handle_delete(),
            icon=ft.Icons.CANCEL,
        )
        rename_action = ft.TextButton(
            "Переименовать",
            on_click=lambda _: self.handle_rename(),
            icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED,
        )

        context_dlg = ft.AlertDialog(
            title=self.path.name,
            content=ft.Container(
                ft.ListView(
                    [delete_action, rename_action],
                    width=500,
                ),
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda _: self.page.close(context_dlg))
            ],
        )
        self.page.open(context_dlg)

    def handle_delete(self):
        if not self.can_be_deleted_or_renamed(True):
            return

        def do_delete(*_):
            self.delete_path()
            self.page.close(dlg)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                f'Удалить {"папку" if self.path.is_dir() else "файл"} "{self.path.name}"?'
            ),
            actions=[
                ft.TextButton(
                    "Удалить",
                    on_click=do_delete,
                ),
                ft.TextButton("Не удалять", on_click=lambda _: self.page.close(dlg)),
            ],
        )

        self.page.open(dlg)

    def delete_path(self):
        if not self.can_be_deleted_or_renamed(True):
            return

        if self.is_in_trash():
            if self.path.is_dir():
                shutil.rmtree(self.path)
            else:
                self.path.unlink()
        else:
            self.system.trash.add(self.path)
            name = self.path.name
            self.path = Path(self.system.trash.path / name)

        self.row.parent.controls.remove(self.row)
        self.page.update()

    def handle_arrow_right(self, event: ft.KeyboardEvent):
        if not event.ctrl and self.path.is_dir():
            self.page.go(str(self.path))

    def handle_rename(self):
        if not self.can_be_deleted_or_renamed(True):
            return
        
        FolderRowItemRenameDialog(self)


class FolderView(BaseView):
    row_items: list[FolderRowItem]
    selected_row_container_index: None | int

    def __init__(self, page: ft.Page, system: System, events: AppEvents):
        super().__init__(page=page, system=system, events=events)

        self.row_items = []
        self.selected_row_container_index = None

        events.keyboard.subscribe(self.handle_keyboard)

    def on_mounted(self):
        self.build_view()

    def on_unmount(self):
        pass

    def build_view(self):
        self.path = Path(self.page.route)

        if not self.path.exists():
            dlg = ft.AlertDialog(
                title=ft.Text(f'Указанный путь "{self.path.resolve()}" не существует')
            )
            self.path = Path(self.system.root_path)
            self.page.open(dlg)

        self.columns_data = FolderColumns()

        self.row_items = [
            FolderRowItem(
                path=path,
                cols_count=self.columns_data.cols_count,
                page=self.page,
                system=self.system,
            )
            for path in self.path.iterdir()
        ]

        view_content = [
            self.columns_data.columns_view,
            ft.ListView(
                controls=[row_item.row for row_item in self.row_items], height=500
            ),
        ]

        self.view = ft.Column(view_content, spacing=0)
        self.title = str(self.path)

    def handle_keyboard(self, event: ft.KeyboardEvent):
        if event.key == "Delete":
            self.handle_delete(event)

        if event.key == "Arrow Up":
            self.handle_arrow_up_or_down(event, direction="up")

        if event.key == "Arrow Down":
            self.handle_arrow_up_or_down(event, direction="down")

        if event.key == "Arrow Right":
            self.handle_arrow_right(event)

        if event.key == "F2":
            self.handle_f2(event)

    def get_selected_rows(self):
        return [
            row_item for row_item in self.row_items if row_item.get_selected_state()
        ]

    def get_first_selected_row(self):
        selected_rows = self.get_selected_rows()
        if len(selected_rows) < 1:
            return None

        return selected_rows[0]

    def handle_delete(self, event: ft.KeyboardEvent):
        for row_item in self.get_selected_rows():
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

    def handle_arrow_right(self, event: ft.KeyboardEvent):
        first_selected = self.get_first_selected_row()
        if not first_selected:
            return

        first_selected.handle_arrow_right(event)

    def handle_f2(self, event: ft.KeyboardEvent):
        first_selected = self.get_first_selected_row()
        if not first_selected:
            return

        first_selected.handle_rename()


class FolderViewStyles:
    def __init__(self):
        self.table_border = ft.border.BorderSide(1, "black")
        self.font_size = 18
        self.cell_padding = ft.padding.only(right=15, left=15, top=10, bottom=10)
        self.row_container_bg_color = ft.Colors.WHITE
        self.row_container_bg_color_selected = ft.Colors.BLUE_100
        self.row_container_bg_color_hovered = ft.Colors.GREY_300


folderViewStyles = FolderViewStyles()


class FolderRowItemRenameDialog:
    def __init__(self, row_item: FolderRowItem):
        self.row_item = row_item

        icon = icon = (
            ft.Icons.FOLDER if self.row_item.path.is_dir() else ft.Icons.FILE_OPEN
        )
        self.text_field = ft.TextField(
            label="Название",
            value=self.row_item.path.name,
            hint_text="Новое название",
            icon=icon,
            on_change=self.handle_change,
            on_submit=lambda _: self.try_save(),
            autofocus=True,
            width=500,
        )

        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Переименовать {self.row_item.path.name}"),
            content=ft.ResponsiveRow([self.text_field]),
            actions=[
                ft.TextButton("Сохранить", on_click=lambda _: self.try_save()),
                ft.TextButton(
                    "Отмена", on_click=lambda _: self.row_item.page.close(self.dlg)
                ),
            ],
        )

        self.row_item.page.open(self.dlg)

    def handle_change(self, event):
        self.text_field.error_text = None
        self.row_item.page.update()

    def try_save(self):
        incorrectMsg = f"Недопустимое название {"папки" if self.row_item.path.is_dir() else "файла"}"

        # допустимое имя файла - изменить
        try:
            self.row_item.path = self.row_item.path.rename(self.text_field.value)
            self.row_item.update_data()
            self.row_item.page.close(self.dlg)
        # имя файла недопустимо - выдать ошибку
        except:
            self.text_field.error_text = incorrectMsg
            self.row_item.page.update()

        self.row_item.page.update()
