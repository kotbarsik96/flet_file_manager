import flet as ft, datetime
from pathlib import Path
from AppContext import AppContext

default_path = "."

class FolderView:
    def __init__(self, app: AppContext):
        self.page = app.page
        self.build_view()

    def map_scandir(self, item: Path):
        extension = "Папка" if item.is_dir() else "Файл ." + item.name.split(".")[-1]

        formatDatetime = "%d.%m.%Y, %H:%M:%S"
        created = datetime.datetime.fromtimestamp(item.stat().st_birthtime).strftime(
            formatDatetime
        )
        updated = datetime.datetime.fromtimestamp(item.stat().st_mtime).strftime(
            formatDatetime
        )
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item.name)),
                ft.DataCell(ft.Text(extension)),
                ft.DataCell(ft.Text(created)),
                ft.DataCell(ft.Text(updated)),
            ],
        )


        if item.is_dir():
            row.on_select_changed = lambda _: self.page.go(str(item.absolute()))

        return row

    def route_to_path(self):
        return str(Path(self.page.route).absolute())
    
    def build_view(self):
        path = self.route_to_path()
        it = Path(path)
        if not it.exists():
            it = Path(default_path)
            dlg = ft.AlertDialog(
                title=ft.Text(f"Указанный путь \"{path}\" не существует")
            )
            self.page.open(dlg)
            
        columns = [
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Тип")),
            ft.DataColumn(ft.Text("Дата создания")),
            ft.DataColumn(ft.Text("Дата изменения")),
        ]
        rows = list(
            map(
                self.map_scandir,
                it.iterdir(),
            )
        )

        self.view = ft.Column(
            [
                ft.DataTable(
                    columns=columns,
                    rows=rows,
                )
            ],
        )