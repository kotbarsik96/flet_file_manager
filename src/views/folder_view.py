import flet as ft, datetime
from pathlib import Path

def FolderView(page: ft.Page):
    def map_scandir(item: Path):
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
            row.on_select_changed = lambda _: page.go(str(item.absolute()))

        return row

    it = Path(page.route)
    columns = [
        ft.DataColumn(ft.Text("Название")),
        ft.DataColumn(ft.Text("Тип")),
        ft.DataColumn(ft.Text("Дата создания")),
        ft.DataColumn(ft.Text("Дата изменения")),
    ]
    rows = list(
        map(
            map_scandir,
            it.iterdir(),
        )
    )

    return ft.Column(
        [
            ft.DataTable(
                columns=columns,
                rows=rows,
            )
        ],
    )
