import flet as ft
from view.layout.blocks.TimerBlocks import TimerOS, TimerApp
from Core import System
from view.layout.blocks.SpaceStatsBlock import SpaceStatsBlock
from Router import Router


class BaseMenuBarDialog:
    dlg: ft.AlertDialog

    def __init__(self, page: ft.Page):
        self.page = page

    def open(self, title, content):
        dlg = ft.AlertDialog(
            title=title,
            content=content,
            actions=[ft.TextButton("Закрыть", on_click=lambda e: self.page.close(dlg))],
        )
        self.page.open(dlg)
        return dlg


class HelpDialog(BaseMenuBarDialog):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        paragraphs = [
            "Файловый менеджер на языке Python с использованием Flet",
            "Разработчик: Никифоров Алексей Владимирович",
            "Группа: ИВТз-43у",
        ]

        content = ft.Column(controls=[])
        for paragraph in paragraphs:
            content.controls.append(ft.Text(paragraph, size=18))

        self.dlg = self.open(ft.Text("О программе"), content)


class HotkeysDialog(BaseMenuBarDialog):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        paragraphs = [
            "– Стрелки вверх-вниз: навигация по доступным кнопкам в приложении",
            "– Стрелка вправо при выделенном элементе - открыть папку/файл (если поддерживается)",
            "– CTRL + Стрелка влево: перейти на предыдущую страницу",
            "– CTRL + Стрелка вправо: перейти на следующую страницу",
            "– F3: Открыть справку по горячим клавишам",
            "– F4: Перейти в папку system",
            "– F5: Открыть статистику по пространству текущего раздела диска",
            "– F6: Открыть встроенный терминал",
            "– F7: Открыть время работы системы",
            "– CTRL + F7: Открыть время работы приложения",
        ]

        content = ft.Column(controls=[])
        for paragraph in paragraphs:
            content.controls.append(ft.Text(paragraph, size=18))

        self.dlg = self.open(title=ft.Text("Горячие клавиши"), content=content)


class OSTimeDialog(BaseMenuBarDialog):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        timer = TimerOS(page)
        self.dlg = self.open(ft.Text("Время работы системы"), timer.timer_text)
        self.dlg.on_dismiss = timer.on_unmount


class AppTimeDialog(BaseMenuBarDialog):
    def __init__(self, page: ft.Page, system: System):
        super().__init__(page)

        timer = TimerApp(page, system)
        self.dlg = self.open(ft.Text("Время работы приложения"), timer.timer_text)
        self.dlg.on_dismiss = timer.on_unmount


class SpaceStatsDialog(BaseMenuBarDialog):
    def __init__(self, page: ft.Page, system: System, router: Router):
        super().__init__(page)

        self.block = SpaceStatsBlock(page, system, router)
        self.dlg = self.open(
            title=ft.Text("Статистика"),
            content=self.block.view,
        )
