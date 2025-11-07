import flet as ft
from Events import AppEvents
from view.FolderView import FolderView
from Core import System


class Router:
    history_backward = []
    history_forward = []
    current_route: str | None = None

    def __init__(self, page: ft.Page, events: AppEvents, system: System):
        self.page = page
        self.events = events
        self.system = system
        self.body = ft.Container(margin=ft.margin.only(bottom=50, top=25))

    def on_route_change(self, route: ft.RouteChangeEvent):
        prev_route = self.get_previuos_route()
        next_route = self.get_next_route()

        is_forward = False
        is_backward = route.route and prev_route and route.route == prev_route
        is_forward = route.route and next_route and route.route == next_route

        # обычный переход - не назад и не вперёд
        if not is_forward and not is_backward:
            if self.current_route:
                self.history_backward.append(self.current_route)
            self.history_forward.clear()
            self.current_route = route.route
        # переход назад
        elif is_backward:
            self.history_forward.insert(0, self.current_route)
            self.current_route = prev_route
            self.history_backward.pop()
        # переход вперёд
        elif is_forward:
            self.history_backward.append(self.current_route)
            self.current_route = next_route
            self.history_forward.pop(0)

        self.view = self.create_view(route)
        self.body.content = self.view.view
        self.body.update()
        self.events.route_changed.trigger(
            route=route.route, is_forward=is_forward, is_backward=is_backward
        )

    def create_view(self, route: ft.RouteChangeEvent):
        return FolderView(page=self.page, system=self.system)

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

    def go_prev_route(self):
        if len(self.history_backward) > 0 and self.history_backward[-1]:
            self.page.go(self.history_backward[-1])

    def go_next_route(self):
        if len(self.history_forward) > 0 and self.history_forward[0]:
            self.page.go(self.history_forward[0])
