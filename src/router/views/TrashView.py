import flet as ft

from router.views.BaseView import BaseView

class TrashView(BaseView):
    def build_view(self):
        self.view = ft.Text("Корзина!!")