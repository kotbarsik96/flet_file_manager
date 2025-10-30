import flet as ft

from views.folder_view import FolderView


class FletRouter:
    history_backward = []
    history_forward = []
    history_current: str | None = None

    def __init__(self, page: ft.Page, ft: ft):
        self.page = page
        self.ft = ft
        self.body = ft.Container()

    def get_previuos_route(self):
        if len(self.history_backward) > 0:
            return self.history_backward[-1]
        else:
            return None

    def get_next_route(self):
        if len(self.history_forward) > 0:
            return self.history_forward[0]
        else:
            return None

    def route_change(self, route):
        prev_route = self.get_previuos_route()
        next_route = self.get_next_route()

        # обычный переход - не назад и не вперёд
        if route.route and route.route != prev_route and route.route != next_route:
            if self.history_current:
                self.history_backward.append(self.history_current)
            self.history_forward.clear()
            self.history_current = route.route
        # переход назад
        elif prev_route and route.route == prev_route:
            self.history_forward.insert(0, self.history_current)
            self.history_current = prev_route
            self.history_backward.pop()
        # переход вперёд
        elif next_route and route.route == next_route:
            self.history_backward.append(self.history_current)
            self.history_current = next_route
            self.history_forward.pop(0)

        self.body.content = FolderView(self.page)
        self.body.update()
