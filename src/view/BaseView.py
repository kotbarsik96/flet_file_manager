import flet as ft
from abc import ABC, abstractmethod
from Core import System
from Events import AppEvents


class BaseView(ABC):
    view: ft.Control

    def __init__(
        self, page: ft.Page, system: System, events: AppEvents, title: str | None = None
    ):
        self.page = page
        self.system = system
        self.events = events
        self.title = title

    @abstractmethod
    def on_mounted(self):
        """Выполняет логику при переходе на этот маршрут (смене View на экземпляр текущего класса)"""

    @abstractmethod
    def on_unmount(self):
        """Выполняет логику при переходе на другой маршрут (смене View)"""

    @abstractmethod
    def build_view(self):
        """Создаёт view и записывает его в self.view"""
