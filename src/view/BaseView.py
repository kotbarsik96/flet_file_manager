import flet as ft
from abc import ABC, abstractmethod


class BaseView(ABC):
    view: ft.Control

    @abstractmethod
    def build_view():
        """Создаёт view и записывает его в self.view"""
